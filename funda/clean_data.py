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
        # m³ removed from parcelsurface  
        data['parcelsurface'] = data['parcelsurface'].str.replace(r'\D', '').astype(int)

        return data
    
    # © Felicia Betten
    def calculate_mean_yearofbuilding_funda_2020(self, date):
        date = date.replace('After ', '') # replace 'After ' with empty
        date = date.replace('Before ', '') # replace 'Before ' with empty
        if "-" in date: # check whether there is a '-' in the column
            date = date.split("-") # if yes, split the two dates
            date = (int(date[0]) + int(date[1])) / 2 # calculate the mean of the two dates
            return(int(date)) # return the mean date
        else:
            return int(date) # if not, return the only date

        # apply function to each row of the column 
        data['yearofbuilding'].apply(lambda date: self.calculate_mean_yearofbuilding_funda_2020(date))
        print("Funda data 2020 cleaned")

    # © Robin Kratschmayr
    def clean_broker_info(data):
        #dropping columns url & replacing the word 'missing' with a 0 to be able to transform col as integer
        data = data.drop(columns=['url']).replace('Missing',np.nan)
        #replacing the whitespace in the middle of the postcode to be able to link with other cbs data
        data['zipcode_broker'] = data.zipcode_broker.replace(" ", "", regex=True)
        #removing unnecessary whitespaces in the broker description
        data['description_broker'] = data.description_broker.replace("  ", " ", regex=True)
        data['description_broker'] = data.description_broker.replace("   ", " ", regex=True)
        data['description_broker'] = data.description_broker.replace("    ", " ", regex=True)
        #specifying the datatypes of each column
        type_dict = {'name_broker': 'string',
            'zipcode_broker':'string',
            'description_broker': 'string',
            'score_broker': 'float64',
            'number_reviews_broker': 'Float64',# has to be converted to float since the column contains NaN values that are not convertible to int
            'number_houses_for_sale_offered': 'Float64',
            'number_houses_sold_last_12_months': 'Float64',
            }

        for k,v in type_dict.items():
            data = data.astype({k: v})

        return data

    # © Robin Kratschmayr
    def clean_broker_reviews(data):
        #shortening the reviewtype
        data['ReviewType'] = data.ReviewType.replace(" reviews","",regex=True)
        #renaming the column Reviewtype to a more accurate name
        data = data.rename(columns={'SalesAgent':'Broker'})
        #transforming the reviewdate into datetimeformat
        data['ReviewDate'] = pd.to_datetime(data['ReviewDate'])
        return data
