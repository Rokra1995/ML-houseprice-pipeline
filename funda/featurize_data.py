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
    # create column with publication month
    data['publicationMonth'] = pd.DatetimeIndex(data['publicationDate']).month
    # create column with publication day
    data['publicationDate'] = pd.DatetimeIndex(data['publicationDate']).day
    # dummy code categoryObject & energylabelClass
    data = pd.get_dummies(data=data, columns=['categoryObject', 'energylabelClass'])
    # drop columns sellingTime and selling date
    data = data.drop(columns=['sellingPrice', 'sellingTime', 'sellingDate'])
    # combine csv files funda_2018 and pc6-gwb2020 (postcodes), join them on zipcode
    data = data.join(data.set_index('zipcode'), on='zipcode')
    # combine csv files funda_2018, pc6-gwb2020 and brt, join them on NeighborhoodCode
    # right: use only keys from right frame, similar to a SQL right outer join; preserve key order.
    data = data.merge(data, on='NeighborhoodCode', how='right')
    # drop columns NeighborhoodCode, DistrictCode_x, Municipalitycode_x and exclude _y from columns names
    data = data.drop(columns=['NeighborhoodCode', 'DistrictCode_x', 'Municipalitycode_x']).rename(columns={'Municipalitycode_y':'Municipalitycode', 'DistrictCode_y':'DistrictCode'})
    
    # option to dummy code the types of houseType seperating by space, but that's not optimal
    # funda_2018_cleaned['houseType'].str.get_dummies(sep=' ').columns


    return data