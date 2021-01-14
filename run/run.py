import json
import os
import datetime
from pathlib import Path
import shutil
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from funda.load_data import DataLoader
from funda.clean_data import DataCleaner
from funda.featurize_data import Featurizer
from funda.partition_data import DataPartitioner
from funda.hypertune_model import Hypertuner

#from funda.validation_utils import DataPartitioner
#from funda.hypertuning import Hypertuner
#from sklearn.ensemble import RandomForestRegressor


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
    for i in ['clean', 'logs', 'prepared', 'models', 'predictions']:
        Path(run_folder, i).mkdir(parents=True, exist_ok=True)
    # if the raw folder does not exist, stop and throw an error
    assert os.path.exists(os.path.join(conf['base_folder'], 'raw')), "I can't find the raw folder!"

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
        
    if reload_clean_data is False:
        print("Loading data...")
        # load data
        data_loader = DataLoader(conf['base_folder'])
        funda_2018 = data_loader.load_funda_data_2018()
        funda_2020 = data_loader.load_funda_data_2020()
        cbs_info = data_loader.load_cbs_data()
        cbs_postcodes = data_loader.load_cbs_postcodes()
        crime_info = data_loader.load_crime_data()
        tourist_info = data_loader.load_tourist_info()
        broker_info = data_loader.load_broker_info()

        print("Cleaning data...")
        # clean data
        data_cleaner = DataCleaner()
        funda_2018_cleaned = data_cleaner.clean_funda_2018(data=funda_2018)
        funda_2020_cleaned = data_cleaner.clean_funda_2020(data=funda_2020)
        cbs_info_cleaned = data_cleaner.clean_cbs_info(data=cbs_info)
        cbs_postcodes_cleaned = data_cleaner.clean_cbs_postcodes(data=cbs_postcodes)
        crime_info_cleaned = data_cleaner.clean_crime_info(data=crime_info)
        tourist_info_cleaned = data_cleaner.clean_tourist_info(data=tourist_info)
        broker_info_cleaned = data_cleaner.clean_tourist_info(data=broker_info)

        print("Storing the cleaned data on the disk...")
        # storing the clean data on disk
        funda_2018_cleaned.to_feather(os.path.join(run_folder, 'clean', 'funda_2018.feather'))
        funda_2020_cleaned.to_feather(os.path.join(run_folder, 'clean', 'funda_2020.feather'))
        cbs_info_cleaned.to_feather(os.path.join(run_folder, 'clean', 'cbs_info.feather'))
        cbs_postcodes_cleaned.to_feather(os.path.join(run_folder, 'clean', 'cbs_postcodes.feather'))
        crime_info_cleaned.to_feather(os.path.join(run_folder, 'clean', 'crime_info.feather'))
        tourist_info_cleaned.to_feather(os.path.join(run_folder, 'clean', 'tourist_info.feather'))
        broker_info_cleaned.to_feather(os.path.join(run_folder, 'clean', 'broker_info.feather'))

        print("data loaded, cleaned and saved")
    

    ## CREATE MODELLING FEATURES 
    featurize = Featurizer()

    ## CREATE TRAIN AND TEST SET
    train, test = train_test_split(gt, test_size=0.4)
    '''
    ## CREATE TRAIN AND TEST SETS AND CV SPLITS
    validation_mapping = DataPartitioner().partition_data(power_df)
    validation_mapping.to_feather(os.path.join(run_folder, 
    "prepared", "validation_mapping.feather"))

    ## CREATE MODELLING FEATURES
    featurized_data = Featurizer(housing_info).fit_transform(power_df)
    featurized_data.to_feather(os.path.join(run_folder, "prepared", "features.feather"))

    ## SELECT BEST FORECASTING MODEL WITH 10 FOLD CV ON TRAIN FEATURES
    train_set = featurized_data.merge(validation_mapping.query("test == False")[['LCLid',
    'date']])
    hypertuner_rf = Hypertuner(estimator = RandomForestRegressor(random_state=1234),
    tuning_params = conf["training_params"]["hypertuning"]["RF_params"],
    validation_mapping = validation_mapping
    )  
    '''


if __name__ == "__main__":
    # the main function above is called when the script is
    # called from command line
    main()