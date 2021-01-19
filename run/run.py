import json
import os
import datetime
from pathlib import Path
import shutil
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split

from funda.load_data import DataLoader
from funda.clean_data import DataCleaner
from funda.featurize_data import Featurizer
from funda.partition_data import DataPartitioner
from funda.hypertune_model import Hypertuner
from funda.evaluate_model import Evaluator

from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from matplotlib import pyplot as plt



# important: for the above import to work, the package needs to be
# installed in the conda environment using e.g. pip install -e .
# from the package root, or python setup.py develop.
# See https://godatadriven.com/blog/a-practical-guide-to-using-setup-py/
# for a good guide to this


def main():
    ## PREPPING
    # setting the run id
    run_id_start_time = datetime.datetime.now()

    print(f"Starting with run at time {run_id_start_time}")
    # read in config
    with open('conf.json', 'r') as f:
        conf = json.load(f)

    run_folder = os.path.join(conf['base_folder'], 'run_' + run_id_start_time.strftime("%Y%m%d_%H%M"))
    # make sure we have all folders where the output of the run
    # will be stored
    for i in ['clean', 'logs', 'prepared', 'models', 'predictions','plots']:
        Path(run_folder, i).mkdir(parents=True, exist_ok=True)
    # if the raw folder does not exist, stop and throw an error
    assert os.path.exists(os.path.join(conf['base_folder'], 'data', 'raw')), "I can't find the raw folder!"

    # log config for the run
    with open(os.path.join(run_folder, 'logs', 'run_config.json'), 'w') as f:
        json.dump(conf, f)

    ## LOAD AND CLEAN 
    #or use previously created features
    try:
        reload_clean_data = conf['loading_params']['reload_clean_data']
    except KeyError:
        pass

    if reload_clean_data:
        print("Attempting to reload previously prepared data")
        try:
            # finding the latest run
            runs = [x for x in os.listdir(conf['base_folder']) if x.startswith('run')]
            runs.sort()
            previous_run = runs[-2]
            # loading the log of previous run to check if data can be loaded:
            with open(os.path.join(conf['base_folder'],previous_run,'logs','run_config.json'), 'r') as f:
                conf_prev = json.load(f)
            
            if (conf_prev['training_params']['data_level'] == conf['training_params']['data_level'] and conf_prev['demo_mode'] == conf['demo_mode']):
                # copying over the cleaned data of the previous run
                shutil.copyfile(os.path.join(conf['base_folder'], previous_run, 'prepared', 'all_features.feather'), 
                os.path.join(conf['base_folder'], run_folder, 'prepared', 'all_features.feather'))
                # loading the clean data of the previous run
                all_features = pd.read_feather(os.path.join(run_folder, 'prepared', 'all_features.feather'))
                print("previously prepared features reloaded")
            else:
                raise Exception('Cannot load features from previous run. Data level differs.')
        except Exception as e:
            print(f'''reloading previously cleaned data failed with error {e}.\n
            Falling back on regenerating clean data.
            ''')
            reload_clean_data = False

    if reload_clean_data is False:
        print("######################## Loading data... ########################")
        # load data
        data_loader = DataLoader(conf['base_folder'])
        funda_2018 = data_loader.load_funda_data_2018()
        funda_2020 = data_loader.load_funda_data_2020()
        if conf['demo_mode']:
            funda_2018 = funda_2018[:1000]
            funda_2020 = funda_2020[:1000]
        zipcodes = data_loader.load_cbs_postcodes()
        brt_data = data_loader.load_brt_2020()
        cbs_info = data_loader.load_cbs_data()
        crime_info = data_loader.load_crime_data()
        tourist_cleaned = data_loader.load_tourist_info()
        broker_info = data_loader.load_broker_info()

        print("######################## Cleaning data... ########################")
        # clean data
        data_cleaner = DataCleaner()
        funda_2018_cleaned = data_cleaner.clean_funda_2018(funda_2018)
        zipcode_data_cleaned = data_cleaner.clean_cbs_postcodes(zipcodes)
        brt_data_cleaned = data_cleaner.clean_brt_2020(brt_data)
        funda_2020_cleaned = data_cleaner.clean_funda_2020(funda_2020)
        cbs_cleaned = data_cleaner.clean_cbs_info(cbs_info)
        crime_cleaned = data_cleaner.clean_crime_info(crime_info)
        broker_cleaned = data_cleaner.clean_broker_info(broker_info)

        ## CREATE MODELLING FEATURES
        print("######################## creating features... ########################") 
        featurize = Featurizer()
        funda = featurize.funda(funda_2018_cleaned, funda_2020_cleaned,zipcode_data_cleaned, brt_data_cleaned,conf['training_params']['data_level'])
        cbs_ft = featurize.cbs_data(crime_cleaned, tourist_cleaned, cbs_cleaned)
        broker_ft = featurize.broker_info(broker_cleaned)
        all_features = featurize.combine_featurized_data(funda, cbs_ft,broker_ft,conf['training_params']['data_level']).reset_index()
        all_features.to_feather(os.path.join(run_folder, 'prepared', 'all_features.feather'))
        print("######################## all features are created ########################")

    ## CREATE TRAIN AND TEST SET
    ## PARTITION DATA
    print("######################## split data into train, test and cross val sets ########################")
    data_partitioner = DataPartitioner(perc_test = conf['training_params']['perc_test'], train_cv_splits = conf['training_params']['train_cv_splits'], seed = conf['training_params']['seed'])
    train_test_set_map = data_partitioner.partition_data(all_features[['index','sellingPrice']]).drop(columns='sellingPrice')
    train_test_set = all_features.merge(train_test_set_map, how="inner", on="index").drop(columns="index")
    train_set = train_test_set[train_test_set.test==False].drop(columns=['test'])
    test_set = train_test_set[train_test_set.test==True].drop(columns=['test'])
    truth = test_set.sellingPrice
    test_set = test_set.drop(columns=['sellingPrice','cv_split'])
    print("######################## data sucessfully split ########################")

    train_set = train_set.drop(columns=['GM2020'])
    test_set_map = test_set[['GM2020']]
    test_set = test_set.drop(columns=['GM2020'])

    print("######################## Building & training & hypertune Random Forest Model ########################")
    ## CREATE RF REGRESSOR AND HYPTERTUNE
    hypertuner_RF = Hypertuner(estimator = RandomForestRegressor(random_state=1234), tuning_params = conf['training_params']['hypertuning']['RF_params'], run_folder= run_folder)

    ## RUN MODEL
    best_model_RF, best_model_mse_RF, best_model_params_RF = hypertuner_RF.tune_model(train_set)
    
    print('#### perfoming prediction on Random Forest Model')
    ## make prediction
    result_RF = best_model_RF.predict(test_set)

    print('#### Evaluating Random Forest')
    evaluate_RF = Evaluator(conf['base_folder'],run_folder,'Random_Forest_Regressor',best_model_params_RF)
    evaluate_RF.evaluate_model(result_RF,truth)
    evaluate_RF.evaluate_on_map(result_RF, truth, test_set_map,'accuracy_5')
    evaluate_RF.evaluate_on_map(result_RF, truth, test_set_map,'accuracy_10')

    print("######################## Building & training Neural Network ########################")
    ## CREATE NN REGRESSOR AND HYPTERTUNE
    hypertuner_NN = Hypertuner(estimator = MLPRegressor(activation='relu',solver='adam'), tuning_params = conf['training_params']['hypertuning']['NN_params'], run_folder= run_folder)
    ## RUN MODEL
    best_model_NN, best_model_mse_NN, best_model_params_NN = hypertuner_NN.tune_model(train_set)
    
    print('#### perfoming prediction on Neural Network')
    ## make prediction
    result_NN = best_model_NN.predict(test_set)

    print('#### Evaluating Neural Network Model')
    evaluate_NN = Evaluator(conf['base_folder'],run_folder,'Neural_Network_Regressor',best_model_params_NN)
    evaluate_NN.evaluate_model(result_NN,truth)
    evaluate_NN.evaluate_on_map(result_NN, truth, test_set_map,'accuracy_5')
    evaluate_NN.evaluate_on_map(result_NN, truth, test_set_map,'accuracy_10')

    print('######################## Models succesfully created, trained and evaluated ########################')
    print('Model, log and plots can be found in the following folder:')
    print(run_folder)
    runtime = datetime.datetime.now() - run_id_start_time
    print('######################## Runtime: '+ str(runtime)+ ' ########################')
    


if __name__ == "__main__":
    # the main function above is called when the script is
    # called from command line
    main()