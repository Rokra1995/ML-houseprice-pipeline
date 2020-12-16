'''Contains classes to load data
'''
import pandas as pd

class DataLoader(object):

    def __init__(self, base_folder):
        self.base_folder = base_folder

    #Emmanuel
    def load_funda_data_2018(self):
        # here the code to load raw data from base folder is implemented
        raise NotImplementedError('Not yet implemented')
    
    #Robin
    def load_funda_data_2020(self):
        full_path = os.path.join(base_folder, 'data/raw/funda_2020_sold_houses.csv')
        data = pd.read_csv(full_path)
        return data

    #Emmanuel
    def load_broker_info(self):
        # here the code to load raw data from base folder is implemented
        raise NotImplementedError('Not yet implemented')
    
    #Robin
    def load_broker_reviews(self):
        # here the code to load raw data from base folder is implemented
        raise NotImplementedError('Not yet implemented')
    
    #Emmanuel
    def load_cbs_data(self):
        # here the code to load raw data from base folder is implemented
        raise NotImplementedError('Not yet implemented')
    
    #Robin
    def load_cbs_postcodes(self):
        # here the code to load raw data from base folder is implemented
        raise NotImplementedError('Not yet implemented')
    
    def load_funda_images(self):
        # here the code to load raw data from base folder is implemented
        raise NotImplementedError('Not yet implemented')
