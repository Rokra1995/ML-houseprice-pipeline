'''This module contains classes to clean the Funda 2020 data 
''' 

import pandas as pd
import numpy as np

df_funda_2020 = pd.read_csv(r'C:\Users\User\Google Drive\Master DDB\AI for Business\product3team2\data\raw\funda_2020_sold_houses.csv')
# check first 5 rows of dataset
df_funda_2020.head()
# check data types of all variables
df_funda_2020.dtypes

# replace every NaN with Missing
df_funda_2020.fillna("Missing",inplace=True)

# replace all values "None" with NaN
df_funda_2020.replace(to_replace="None", value=np.nan, inplace=True)

# show all columns having NaN values
df_funda_2020.isnull().sum()
''' Facilities              92964
    Cadastre_Title          13015
    Ownership situation     53580
    description_garden      31328
    energylabelclass        10324
    buying_agent           182251
Suggestion: drop these (a few of these) columns
'''

# To do: integrate these functions in Class