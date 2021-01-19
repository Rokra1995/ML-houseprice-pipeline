'''This module contains a class with features
'''

import pandas as pd
import numpy as np
import re

class Featurizer(object):
    
    def __init__(self):
        pass

    # © Felicia Betten
    def funda(self, funda_2018, funda_2020,zipcode_data, brt_data, data_level):
        ## CREATE FUNDA 2018 FEATURES

        ### create column with publication day, month and year
        funda_2018['publicationDay'] = pd.DatetimeIndex(funda_2018['publicationDate']).day
        funda_2018['publicationMonth'] = pd.DatetimeIndex(funda_2018['publicationDate']).month
        funda_2018['publicationYear'] = pd.DatetimeIndex(funda_2018['publicationDate']).year
        ### drop columns publicationDate, sellingPrice, sellingTime and sellingDate
        funda_2018 = funda_2018.drop(columns=['publicationDate', 'sellingTime', 'sellingDate'])
        funda_2018['houseType'] = funda_2018['houseType'].replace(to_replace={'2-onder-1-kapwoning':'semi-detachedresidentialproperty','bel-etage':'Ground-floorapartment','beneden+bovenwoning':'Ground-floor+upstairsapartment', 'benedenwoning':'Residentialpropertywithsharedstreetentrance', 'bovenwoning':'Upstairsapartment', 'bungalow':'Bungalow', 'dubbelbenedenhuis':'Doubleground-floorapartment', 'eengezinswoning':'Single-familyhome', 'galerijflat':'Galleriedapartment', 'geschakelde2-onder-1-kapwoning':'linkedsemi-detachedresidentialproperty', 'grachtenpand':'Propertyalongsidecanal', 'halfvrijstaandewoning':'detachedresidentialproperty', 'hoekwoning':'cornerhouse', 'penthouse':'Penthouse', 'landgoed':'Countryestate', 'landhuis':'Countryhouse', 'maisonnette':'Maisonnette', 'stacaravan':'Mobilehome', 'semi-bungalow':'semi-detachedresidentialproperty', 'verspringend':'staggered', 'studentenkamer':'Studentroom', 'tussenverdieping':'Mezzanine', 'villa':'Villa', 'vrijstaandewoning':'Desirableresidence/villa', 'woonboerderij':'Convertedfarmhouse', 'woonboot':'Houseboat', 'OpenPortiek':'Apartmentwithsharedstreetentrance', 'OpenPortiek2':'Apartmentwithsharedstreetentrance', 'portiekflat':'Apartmentwithsharedstreetentrance', 'portiekwoning':'Apartmentwithsharedstreetentrance', 'dubbelbovenhuis':'doublehouse', 'appartement':'Apartmentwithsharedstreetentrance', 'bedrijfs-ofdienstwoning':'companyresidenceofficialresidence', 'corridorflat':'Apartmentwithsharedstreetentrance', 'dijkwoning':'dykehouse', 'drive-inwoning':'drive-in house', 'eindwoning':'Apartmentwithsharedstreetentrance', 'geschakeldewoning':'semi-detachedresidentialproperty', 'herenhuis':'mansion', 'hofjeswoning':'Countryhouse', 'kwadrantwoning':'quadranthouse', 'paalwoning':'stilthouse', 'patiowoning':'patiohouse', 'split-levelwoning':'split-levelhouse', 'tussenwoning':'rowhouse', 'verzorgingsflat':'nursing-home', 'waterwoning':'waterhouse', 'wind/watermolen':'wind/watermill'},regex=True)
        
        if data_level <5:
            funda_data = funda_2018
   
        ## CREATE POSTCODE TO MUNICIPALITY AND NEIGHBORHOODCODE TRANSLATION TABLE
        zipcode_translation = zipcode_data.merge(brt_data, how="left", on="NeighborhoodCode").drop(columns=['DistrictCode_x','MunicipalityCode','MunicipalityName','DistrictName']).rename(columns={'DistrictCode_y':'DistrictCode'}).drop_duplicates()
        zipcode_translation['NeighborhoodCode'] = zipcode_translation['NeighborhoodCode'].astype('object')
        ## CREATE FUNDA 2020 FEATURES

        if data_level >4:
            # create column with publication day, month and year
            funda_2020['publicationDay'] = pd.DatetimeIndex(funda_2020['publicationDate']).day
            funda_2020['publicationMonth'] = pd.DatetimeIndex(funda_2020['publicationDate']).month
            funda_2020['publicationYear'] = pd.DatetimeIndex(funda_2020['publicationDate']).year
            # drop columns publicationDate, sellingPrice, Asking_Price_M2, Facilities, description_garden, sellingDate, sellingtime and url
            # and rename columns to the same names in funda_2018
            funda_2020 = funda_2020.drop(columns=['publicationDate', 'description_garden', 'sellingDate', 'sellingTime']).rename(columns={'fulldescription':'fullDescription', 'yearofbuilding':'yearofbuilding', 'garden_binary':'garden', 'housetype':'houseType', 'parcelsurface':'parcelSurface', 'energylabelclass':'energylabelClass','numberrooms':'numberRooms', 'numberbathrooms':'numberBathrooms'})
            # remove the brackets and its content for housetype
            funda_2020['houseType'] = funda_2020['houseType'].str.replace(r"\(.*\)","").str.lstrip().str.replace('\r\n', '')
            # replace NaN sales_agent and buying_agent with -1
            funda_2020['sales_agent'] = funda_2020['sales_agent'].fillna(-1)
            funda_2020['buying_agent'] = funda_2020['buying_agent'].fillna(-1)
            # concat with funda 2018 data
            funda_data = pd.concat([funda_2018,funda_2020])
        
    
        ## MERGE ALL TOGETHER
        all_data = funda_data.merge(zipcode_translation, how="left", on="zipcode")

        ## DUMMY CODE CATEGORICAL VARIABLES
        # create new dataframe with houseTypes dummy codes
        houseTypes = all_data['houseType'].str.get_dummies(sep=",").add_prefix('houseType_')
        # join houseType_df with funda_2018
        all_data = all_data.join(houseTypes, how='left').drop(axis=1, columns='houseType') 

        #get dummies   
        all_data = pd.get_dummies(data=all_data, columns=['categoryObject', 'energylabelClass'])

        if data_level > 0:
            # create other dummies
            all_data['Municipalitycode_copy'] = all_data['Municipalitycode']
            all_data = pd.get_dummies(data=all_data, columns=['Municipalitycode_copy'])
        if data_level > 1:
            all_data['DistrictCode_copy'] = all_data['DistrictCode']
            all_data = pd.get_dummies(data=all_data, columns=['DistrictCode_copy'])
        if data_level > 2:
            all_data['NeighborhoodCode_copy'] = all_data['NeighborhoodCode']
            all_data = pd.get_dummies(data=all_data, columns=['NeighborhoodCode_copy'])
 
        # replace NaN of parcelsurface with mean per municipalitycode
        all_data['parcelSurface'] = all_data['parcelSurface'].fillna(all_data.groupby('Municipalitycode')['parcelSurface'].transform('mean'))

        all_data = all_data.fillna(-1)
        print('funda features created')
        return all_data

    # © Emmanuel Owusu Annim
    def cbs_data(self, crime_data, tourist_info, cbs_data_old):
        #Fill NAN with Mean & Print new data set called cbs_data
        cbs_data = cbs_data_old.fillna(cbs_data_old.mean())
        cbs_data['Municipalitycode'] = cbs_data['Municipalitycode'].str.strip()
        
        #Merge TouristData & CrimeData together on key 'Municipalitycode'
        merge1 = (pd.merge(crime_data, tourist_info, on='Municipalitycode'))

        #Merge CBS Data with Merge1 and make a complete df of all the data
        all_data = cbs_data.merge(merge1, on='Municipalitycode', how='left').sort_values(['Municipalitycode']).fillna(-1)
        return all_data

   # © Robin Kratschmayr
    @staticmethod
    def broker_info(broker_info):
        broker_features = broker_info.drop(columns=['zipcode_broker','description_broker','url'])
        return broker_features

    # © Robin Kratschmayr
    def combine_featurized_data(self,funda,cbs_ft,broker_ft, data_level):
        if data_level <= 3:
            data = funda.drop(columns=['Municipalitycode','DistrictCode','NeighborhoodCode'])

        if data_level>3:
            # merging all the data
            data = funda.merge(cbs_ft, how="left", on="Municipalitycode")
            data = data.merge(cbs_ft, how="left", left_on="DistrictCode", right_on="Municipalitycode", suffixes=['_GM','_WK'])
            data = data.drop(columns=['Municipalitycode_GM','Municipalitycode_WK','DistrictCode']).fillna(-1)
        if data_level > 5:
            data = data.merge(broker_ft, how="left", left_on="sales_agent", right_on="name_broker")
            data = data.merge(broker_ft, how="left", left_on="buying_agent", right_on="name_broker", suffixes=['_Sale','_Buy'])
            #Drop columns that are not needed and replace ervy NaN with a -1
            data = data.drop(columns=['name_broker_Buy','name_broker_Sale','sales_agent','buying_agent']).fillna(-1)

        #Drop columns that are not needed and replace ervy NaN with a -1
        data = data.drop(columns=['zipcode','fullDescription'])
        data = data.fillna(-1)
        return data