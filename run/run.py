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
    # load the raw data and clean it
    # if the option reload_clean_data is set to true, then reload the clean data
    # from the previous run
    # the whole logic block below could be encapsulated in its own function/class
    reload_clean_data = False
    try:
        reload_clean_data = conf['loading_params']['reload_clean_data']
    except KeyError:
        pass
    reload_clean_data = False 
    if reload_clean_data:
        print("Attempting to reload previously cleaned data")
        try:
            # finding the latest run
            runs = [x for x in os.listdir(conf['base_folder']) if x.startswith('run')]
            runs.sort()
            previous_run = runs[-2]
            # copying over the cleaned data of the previous run
            shutil.copyfile(os.path.join(conf['base_folder'], previous_run, 'clean', 'housing_info.feather'), 
            os.path.join(conf['base_folder'], run_folder, 'clean', 'housing_info.feather'))
            shutil.copyfile(os.path.join(conf['base_folder'], previous_run, 'clean', 'power_df.feather'), 
            os.path.join(conf['base_folder'], run_folder, 'clean', 'power_df.feather'))
            # loading the clean data of the previous run
            housing_info = pd.read_feather(os.path.join(run_folder, 'clean', 'housing_info.feather'))
            power_df = pd.read_feather(os.path.join(run_folder, 'clean', "power_df.feather"))
            print("previously cleaned data reloaded")
        except Exception as e:
            print(f'''reloading previously cleaned data failed with error {e}.\n
            Falling back on regenerating clean data.
            ''')
            reload_clean_data = False
    if conf['data_level'] == 1:
        reload_clean_data == False

    if reload_clean_data is False:
        print("Loading data...")
        # load data
        data_loader = DataLoader(conf['base_folder'])
        funda_2018 = data_loader.load_funda_data_2018()
        funda_2020 = data_loader.load_funda_data_2020()
        if conf['demo_mode'] == 1:
            funda_2018 = funda_2018[:2000]
            funda_2020 = funda_2020[:1000]
        zipcodes = data_loader.load_cbs_postcodes()
        brt_data = data_loader.load_brt_2020()
        cbs_info = data_loader.load_cbs_data()
        crime_info = data_loader.load_crime_data()
        tourist_cleaned = data_loader.load_tourist_info()
        broker_info = data_loader.load_broker_info()

        print("Cleaning data...")
        # clean data
        data_cleaner = DataCleaner()
        funda_2018_cleaned = data_cleaner.clean_funda_2018(funda_2018)
        zipcode_data_cleaned = data_cleaner.clean_cbs_postcodes(zipcodes)
        brt_data_cleaned = data_cleaner.clean_brt_2020(brt_data)
        funda_2020_cleaned = data_cleaner.clean_funda_2020(funda_2020)
        cbs_cleaned = data_cleaner.clean_cbs_info(cbs_info)
        crime_cleaned = data_cleaner.clean_crime_info(crime_info)
        broker_cleaned = data_cleaner.clean_broker_info(broker_info)

        print("Storing the cleaned data on the disk...")
        # storing the clean data on disk
        #funda_2018_cleaned.reset_index().to_feather(os.path.join(run_folder, 'clean', 'funda_2018.feather'))
        #funda_2020_cleaned.to_feather(os.path.join(run_folder, 'clean', 'funda_2020.feather'))
        #cbs_cleaned.to_feather(os.path.join(run_folder, 'clean', 'cbs_info.feather'))
        #zipcode_data_cleaned.to_feather(os.path.join(run_folder, 'clean', 'cbs_postcodes.feather'))
        #crime_cleaned.to_feather(os.path.join(run_folder, 'clean', 'crime_info.feather'))
        #tourist_cleaned.to_feather(os.path.join(run_folder, 'clean', 'tourist_info.feather'))
        #broker_cleaned.to_feather(os.path.join(run_folder, 'clean', 'broker_info.feather'))
        #brt_data_cleaned.to_feather(os.path.join(run_folder, 'clean', 'brt.feather'))

        print("data loaded, cleaned and saved")
    


    ## CREATE MODELLING FEATURES 
    featurize = Featurizer()
    funda = featurize.funda(funda_2018_cleaned, funda_2020_cleaned,zipcode_data_cleaned, brt_data_cleaned,conf['data_level'])
    cbs_ft = featurize.cbs_data(crime_cleaned, tourist_cleaned, cbs_cleaned)
    broker_ft = featurize.broker_info(broker_cleaned)
    all_features = featurize.combine_featurized_data(funda, cbs_ft,broker_ft,conf['data_level']).reset_index()
    funda=0
    cbs_ft=0
    broker_ft=0

    ## CREATE TRAIN AND TEST SET
    ## PARTITION DATA
    data_partitioner = DataPartitioner()
    train_test_set_map = data_partitioner.partition_data(all_features[['index','sellingPrice']]).drop(columns='sellingPrice')
    train_test_set = all_features.merge(train_test_set_map, how="inner", on="index").drop(columns="index")
    train_set = train_test_set[train_test_set.test==False].drop(columns=['test'])
    test_set = train_test_set[train_test_set.test==True].drop(columns=['test'])
    truth = test_set.sellingPrice
    test_set = test_set.drop(columns=['sellingPrice','cv_split'])
    all_features=0

    train_set = train_set.drop(columns=['GM2020'])
    test_set_map = test_set[['GM2020']]
    test_set = test_set.drop(columns=['GM2020'])

    print('Building & training Random Forest Model')
    ## CREATE RF REGRESSOR AND HYPTERTUNE
    hypertuner_rf = Hypertuner(estimator = RandomForestRegressor(random_state=1234), tuning_params = conf['training_params']['hypertuning']['RF_params'], run_folder= run_folder)

    ## RUN MODEL
    tested_models, best_model_mse, best_model_params_RF, best_model_name = hypertuner_rf.tune_model(train_set)
    
    print('perfoming prediction on Random Forest Model')
    ## LOAD MODEL and make prediction
    loaded_model = pickle.load(open(os.path.join(run_folder, 'models' , best_model_name ), 'rb'))
    result_RF = loaded_model.predict(test_set)

    print('Building & training Neural Network')
    ## CREATE NN REGRESSOR AND HYPTERTUNE
    hypertuner_NN = Hypertuner(estimator = MLPRegressor(activation='relu',solver='adam'), tuning_params = conf['training_params']['hypertuning']['NN_params'], run_folder= run_folder)
    ## RUN MODEL
    tested_models, best_model_mse, best_model_params_NN, best_model_name = hypertuner_NN.tune_model(train_set)
    
    print('perfoming prediction on Neural Network')
    ## LOAD MODEL and make prediction
    loaded_model = pickle.load(open(os.path.join(run_folder, 'models' , best_model_name ), 'rb'))
    result_NN = loaded_model.predict(test_set)



    runtime = datetime.datetime.now() - run_id_start_time
    print('Runtime: '+ str(runtime))

    print('Time to evalaute the best of each modeltypes...')
    
    evaluate_RF = Evaluator(conf['base_folder'],run_folder,'Random_Forest_Regressor',best_model_params_RF)
    evaluate_RF.evaluate_model(result_RF,truth)
    evaluate_RF.evaluate_on_map(result_RF, truth, test_set_map,'accuracy_5')
    evaluate_RF.evaluate_on_map(result_RF, truth, test_set_map,'accuracy_10')

    evaluate_NN = Evaluator(conf['base_folder'],run_folder,'Neural_Network_Regressor',best_model_params_NN)
    evaluate_NN.evaluate_model(result_NN,truth)
    evaluate_RF.evaluate_on_map(result_NN, truth, test_set_map,'accuracy_5')
    evaluate_RF.evaluate_on_map(result_NN, truth, test_set_map,'accuracy_10')
    


if __name__ == "__main__":
    # the main function above is called when the script is
    # called from command line
    main()