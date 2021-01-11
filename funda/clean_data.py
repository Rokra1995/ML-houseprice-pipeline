'''This module contains classes to clean the data 
'''

import pandas as pd
import numpy as np

class DataCleaner(object):

    # © Felicia Betten
    def clean_funda_2020(self, data):
        # Replace all None values by NaN
        data = data.replace("None", np.NaN)
        # Drop column Ownership situation
        data.drop(axis=1, columns='Ownership situation')
        # Remove m³ removed from parcelsurface  
        data['parcelsurface'] = data['parcelsurface'].str.replace(r'\D', '').astype(int)
        # Remove \r \n from housetype
        data['housetype'] = data['housetype'].str.rstrip('\r\n')
        # Replace 0 in Garden_binary with NaN
        data['garden_binary'] = data['garden_binary'].replace(0, np.nan)      

        def calculate_mean_yearofbuilding_funda_2020(date):
            date = date.replace('After ', '') # replace 'After ' with empty
            date = date.replace('Before ', '') # replace 'Before ' with empty
            if "-" in date: # check whether there is a '-' in the column
                date = date.split("-") # if yes, split the two dates
                date = (int(date[0]) + int(date[1])) / 2 # calculate the mean of the two dates
                return(int(date)) # return the mean date
            else:
                return int(date) # if not, return the only date

            # apply function to each row of the column 
        data['yearofbuilding'] = data['yearofbuilding'].apply(lambda date: calculate_mean_yearofbuilding_funda_2020(date))
        print("Funda data 2020 cleaned")
        return data
    
    # © Baris Orman
    @staticmethod
    def cleaned_funda_2018(data):
        #Renaming the columns to english
        data = data.fillna(0).drop(['globalId', 'globalId.1','kantoor_naam_MD5hash'], axis=1)

        #HOUSETYPE AND CATEGORYOBJECT: SEPERATE THE VARIABALES WITH COMMA'S AND REMOVE THE BRACKETS
        data['houseType'] = data['houseType'].str.replace('<', "").str.replace('{', "").str.replace('}', "").str.replace('>', "")
        data['categoryObject'] = data['categoryObject'].str.replace('<', "").str.replace('{', "").str.replace('}', "").str.replace('>', "")
        data['fullDescription'] = data['fullDescription'].str.replace("\n", "")

        #Calculation of sellingtime and adding the column
        data['sellingTime'] = pd.to_datetime(data['sellingDate']) - pd.to_datetime(data['publicationDate'])
        data['sellingTime'] = data['sellingTime'].apply(lambda x: int(x.days))

        #Replace the 0 in Parcelsruface with NaN
        data['parcelSurface'] = data['parcelSurface'].replace(0.0, np.nan)

        #CALCULATE THE MEAN OF VERY OLD YEAR OF BUILDINGS
        def mean_yearofBuilding_funda_2018(date):
            date = date.replace('<{Voor}> ', '')
            date = date.replace('<{Na}> ', '')
            if '-' in date:
                date = date.split("-")
                date = (int(date[0]) + int(date[1])) / 2
                return(int(date))
            else:
                return int(date)

        data['yearOfBuilding'] = data['yearOfBuilding'].apply(lambda date: mean_yearofBuilding_funda_2018(date))
        print("Funda data 2018 cleaned")
        return data


    # © Robin Kratschmayr
    @staticmethod
    def clean_broker_info(data):
        #dropping columns url & replacing the word 'missing' with a 0 to be able to transform col as integer
        data = data.replace('Missing',0)
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
    @staticmethod
    def clean_broker_reviews(data):
        #shortening the reviewtype
        data['ReviewType'] = data.ReviewType.replace(" reviews","",regex=True)
        #renaming the column Reviewtype to a more accurate name
        data = data.rename(columns={'SalesAgent':'Broker'})
        #transforming the reviewdate into datetimeformat
        data['ReviewDate'] = pd.to_datetime(data['ReviewDate'])
        return data

    # © Emmanuel Owusu Annim
    @staticmethod
    def clean_tourist_info(data):
        #Translate Dutch Headers to English Headers
        return data
            
    # © Emmanuel Owusu Annim
    @staticmethod
    def clean_crime_info(data):
        #Translate Dutch Headers to English Headers
        return data
            
