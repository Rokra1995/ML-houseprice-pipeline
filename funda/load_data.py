'''Contains classes to load data
'''
import pandas as pd

class DataLoader(object):

    def __init__(self, base_folder):
        self.base_folder = base_folder

    #Emmanuel
    def load_funda_data_2018(self):
        full_path = os.path.join(self.base_folder, 'data/raw/funda_2018.csv')
        data = pd.read_csv(full_path)
        return data
    
    #Robin
    def load_funda_data_2020(self):
        full_path = os.path.join(self.base_folder, 'data/raw/funda_2020_sold_houses.csv')
        data = pd.read_csv(full_path)
        return data

    #Emmanuel
    def load_broker_info(self):
        full_path = os.path.join(self.base_folder, 'data/raw/brokers_2020_info.csv')
        data = pd.read_csv(full_path)
        return data
        
    
    #Robin
    def load_broker_reviews(self):
        full_path = os.path.join(self.base_folder, 'data/raw/brokers_2020_reviews.csv')
        data = pd.read_csv(full_path)
        return data
    
    #Emmanuel
    def load_cbs_data(self):
        full_path = os.path.join(self.base_folder, 'data/raw/CBS_data.csv')
        data = pd.read_csv(full_path, sep=";")
        return data
    
    #Robin
    def load_cbs_postcodes(self):
        full_path = os.path.join(self.base_folder, 'data/raw/pc6-gwb2020.csv')
        data = pd.read_csv(full_path, sep=";")
        return data    
    def load_funda_images(self):
        # here the code to load raw data from base folder is implemented
        raise NotImplementedError('Not yet implemented')
