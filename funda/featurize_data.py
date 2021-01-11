'''This module contains a class with features
'''

import IPython
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error 
import seaborn as sb
#%matplotlib inline
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import warnings 
warnings.filterwarnings('ignore')
warnings.filterwarnings('ignore', category=DeprecationWarning)
import tensorflow as tf
import tensorflow_docs as tfdocs
import tensorflow_docs.plots
import tensorflow_docs.modeling
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten
import datetime

# © Felicia Betten
def featurize_funda_2018 (self, data):
    # create column with publication day, month and year
    funda_2018_cleaned['publicationDay'] = pd.DatetimeIndex(funda_2018_cleaned['publicationDate']).day
    funda_2018_cleaned['publicationMonth'] = pd.DatetimeIndex(funda_2018_cleaned['publicationDate']).month
    funda_2018_cleaned['publicationYear'] = pd.DatetimeIndex(funda_2018_cleaned['publicationDate']).year
    # dummy code categoryObject & energylabelClass
    pd.get_dummies(data=funda_2018_cleaned, columns=['categoryObject', 'energylabelClass'])
    # drop columns publicationDate, sellingPrice, sellingTime and sellingDate
    funda_2018_cleaned = funda_2018_cleaned.drop(columns=['publicationDate', 'sellingPrice', 'sellingTime', 'sellingDate'])
    # combine csv files funda_2018 and pc6-gwb2020 (postcodes), join them on zipcode
    funda_zipcode_df = funda_2018_cleaned.join(zipcode_data_cleaned.set_index('zipcode'), on='zipcode')
    # combine csv files funda_2018, pc6-gwb2020 and brt, join them on NeighborhoodCode
    # right: use only keys from right frame, similar to a SQL right outer join; preserve key order.
    funda_zipcode_brt_df = funda_zipcode_df.merge(brt_data_cleaned, on='NeighborhoodCode', how='right')
    # drop columns NeighborhoodCode, DistrictCode_x, Municipalitycode_x and exclude _y from columns names
    funda_zipcode_brt_df = funda_zipcode_brt_df.drop(columns=['NeighborhoodCode', 'DistrictCode_x', 'Municipalitycode_x']).rename(columns={'Municipalitycode_y':'Municipalitycode', 'DistrictCode_y':'DistrictCode'})
    
    # create new dataframe with houseTypes dummy codes
    houseTypes_df = funda_2018_cleaned['houseType'].str.get_dummies(sep=",")
    # join houseType_df with funda_2018
    joined_df = funda_2018_cleaned.join(houseTypes_df, how='right').drop(axis=1, columns='houseType')
    # combine csv files funda_2018, pc6-gwb2020 (postcodes), join them on zipcode
    funda_zipcode_df = joined_df.join(zipcode_data_cleaned.set_index('zipcode'), on='zipcode')
    # combine csv files funda_2018, pc6-gwb2020 and brt, join them on NeighborhoodCode
    # right: use only keys from right frame, similar to a SQL right outer join; preserve key order.
    funda_zipcode_brt_df = funda_zipcode_df.merge(brt_data_cleaned, on='NeighborhoodCode', how='right')
    # drop columns NeighborhoodCode, DistrictCode_x, Municipalitycode_x, NeighborhoodName, MunicipalityName and DistrictName and exclude _y from columns names
    funda_zipcode_brt_df = funda_zipcode_brt_df.drop(columns=['NeighborhoodCode', 'DistrictCode_x', 'Municipalitycode_x', 'NeighborhoodName', 'MunicipalityName', 'DistrictName']).rename(columns={'Municipalitycode_y':'Municipalitycode', 'DistrictCode_y':'DistrictCode'})
    # replace NaN in parcelSurface with the mean of the Municpality 
    funda_zipcode_brt_df['parcelSurface'] = funda_zipcode_brt_df.groupby("Municipalitycode").transform(lambda x: x.fillna(x.mean()))
    # dummy code Municipalitycode and DistrictCode
    funda_zipcode_brt_df = pd.get_dummies(funda_zipcode_brt_df, columns=['Municipalitycode', 'DistrictCode'])

    return funda_zipcode_brt_df