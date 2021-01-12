import pandas as pd
import numpy as np

class Featurizer(object):

    # © Felicia Betten
    @staticmethod
    def featurize_funda_data(data):

        return data

    # © Emmanuel Owusu Annim
    @staticmethod
    def featurize_cbs_data(crime_data, tourist_info, cbs_data_old):
    #Here I fill NAN values with the MEAN and I printed a new data set called cbs_data

    cbs_data = cbs_data_old.fillna(cbs_data_old())
    cbs_data['Municipalitycode'] = cbs_data['Municipalitycode'].str.strip()

    #Here I merged the other data sets TouristData & Crimedata together on the key 'Municipalitycode'
    merge1 = (pd.merge(crime_data, tourist_info, on='Municipalitycode'))

    #Here I merged the dataset cbs_data with Merge1 and make a complete datasett of all the data
    all_data = cbs_data.merge(merge1, on='Municipalitycode', how='inner').sort_values(['Municipalitycode'])
    
        return all_data

   # © Robin Kratschmayr
    @staticmethod
    def featurize_broke_info(broker_info):
        broker_features = broker_info.drop(columns=['zipcode_broker','description_broker','url'])
        return broker_features

    # © to be discussed
    @staticmethod
    def combine_featurized_data(funda,cbs,brokers):
        pass

