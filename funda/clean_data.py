'''This module contains classes to clean the Funda 2020 data 
''' 

import pandas as pd
import numpy as np


class DataCleaner(object):

    # © Felicia Betten
    def clean_funda_2020(self, data):
        # Replace all None values by NaN
        data = data.replace(to_replace="None", value=np.nan, inplace=True)
        # Drop column Ownership situation
        data.drop(axis=1, columns='Ownership situation')
        # Remove m³ removed from parcelsurface  
        data['parcelsurface'] = data['parcelsurface'].str.replace(r'\D', '').astype(int)

        return data

    def calculate_mean_yearofbuilding_funda_2020(self, date):
        date = date.replace('After ', '') # replace 'After ' with empty
        date = date.replace('Before ', '') # replace 'Before ' with empty
        if "-" in date: # check whether there is a '-' in the column
            date = date.split("-") # if yes, split the two dates
            date = (int(date[0]) + int(date[1])) / 2 # calculate the mean of the two dates
            return(int(date)) # return the mean data
        else:
            return int(date) # if not, return the only date

        # apply function to each row of the column 
        data['yearofbuilding'].apply(lambda date: self.calculate_mean_yearofbuilding_funda_2020(date))
        print("Funda data 2020 cleaned")