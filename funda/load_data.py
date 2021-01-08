'''Contains classes to load data
'''
import pandas as pd
import numpy as np
import os

class DataLoader(object):

    def __init__(self, base_folder):
        self.base_folder = base_folder  

    #Emmanuel
    def load_funda_data_2018(self):
        full_path = os.path.join(self.base_folder, 'data','raw','funda_2018.csv')
        data = pd.read_csv(full_path, dtype=self.funda_2018_dtypes)
        
        #RENAMING COLUMNS INTO ENGLISH
        data = data.rename(columns={'publicatieDatum':'publicationDate','postcode':'zipcode', 'koopPrijs':'sellingPrice',\
          'volledigeOmschrijving':'fullDescription','soortWoning':'houseType','categorieObject':'categoryObject', 'bouwjaar':'yearOfBuilding', \
          'indTuin':'garden','perceelOppervlakte':'parcelSurface','aantalKamers':'numberRooms','aantalBadkamers':'numberBathrooms',   'energielabelKlasse':'energylabelClass',\
          'oppervlakte':'surface','datum_ondertekening':'sellingDate'})

        #Changing dataypes for publication date and selling date
        data['publicationDate'] = pd.to_datetime(data['publicationDate'])
        data['sellingDate'] = pd.to_datetime(data['sellingDate'])
        print('Funda data of 2018 successfully loaded')
        return data
    
    #Robin
    def load_funda_data_2020(self):
        full_path = os.path.join(self.base_folder, 'data','raw','funda_2020_sold_houses.csv')
        data = pd.read_csv(full_path)    
        print('Funda data of 2020 successfully loaded')
        return data

    #Emmanuel
    def load_broker_info(self):
        full_path = os.path.join(self.base_folder, 'data', 'raw', 'brokers_2020_info.csv')
        data = pd.read_csv(full_path)
        data = data.rename(columns={'PC6': 'Zipcode', 'Buurt2020': 'NeighborhoodCode', 'Wijk2020': 'DistrictCode', 'Gemeente2020': 'MunicipalityCode'})
        print('Broker Information successfully loaded')
        return data
        
    #Robin
    def load_broker_reviews(self):
        full_path = os.path.join(self.base_folder, 'data', 'raw', 'brokers_2020_reviews.csv')
        data = pd.read_csv(full_path)
        print('Broker reviews successfully loaded')
        return data
    
    #Emmanuel
    def load_cbs_data(self):
        full_path = os.path.join(self.base_folder, 'data', 'raw', 'CBS_data.csv')
        data = pd.read_csv(full_path, sep=";")
        data = data.rename(columns={'WijkenEnBuurten':'NeighborhoodsAndDistricts','Gemeentenaam_1':'NameOfMunicipality','Mannen_6':'NumberOfMen',\
    'Vrouwen_7':'NumberOfWomen','k_0Tot15Jaar_8':'AgeFrom0to15years','k_15Tot25Jaar_9':'AgeFrom15to25years',\
    'k_25Tot45Jaar_10' : 'AgeFrom25to45years','k_45Tot65Jaar_11' : 'AgeFrom45to65years','k_65JaarOfOuder_12' : 'AgeFrom65AndOlder',\
    'Bevolkingsdichtheid_33' : 'PopulationDensity','Woningvoorraad_34' : 'HousingStock','PercentageBewoond_38' : 'PercentageInhabited',\
    'PercentageOnbewoond_39' : 'PercentageUninhabited','Koopwoningen_40' : 'OwnerOccupiedHouses','HuurwoningenTotaal_41' : 'RentalHouses',\
    'BouwjaarVoor2000_45' : 'ConstructionYearBefore2000','BouwjaarVanaf2000_46' : 'ConstructionYearAfter2000',\
    'GemiddeldInkomenPerInwoner_66' : 'AverageIncomePerCitizen','MeestVoorkomendePostcode_103' : 'MostCommonPostalCode','Dekkingspercentage_104' : 'CoveragePercentage'})
        print('CBS info successfully loaded')
        return data
    
    #Robin
    def load_cbs_postcodes(self):
        full_path = os.path.join(self.base_folder, 'data', 'raw', 'pc6-gwb2020.csv')
        data = pd.read_csv(full_path, sep=";")
        data = data.rename(columns={'PC6': 'Zipcode', 'Buurt2020': 'NeighborhoodCode', 'Wijk2020': 'DistrictCode', 'Gemeente2020': 'MunicipalityCode'})
        print('cbs postcodes successfully loaded')
        return data

    #Robin
    def load_funda_images(self):
        # here the code to load raw data from base folder is implemented
        raise NotImplementedError('Not yet implemented')

    #Emmanuel
    def load_crime_data(self):
        full_path = os.path.join(self.base_folder, 'data', 'raw', 'crime_data.csv')
        data = pd.read_csv(full_path, sep=";")
        data = data.rename(columns={'SoortMisdrijf': 'CrimeType', 'RegioS': 'Municipalitycode', 'Perioden': 'Periods', 'TotaalGeregistreerdeMisdrijven_1': 'Total Registered Crimes', 'GeregistreerdeMisdrijvenRelatief_2': 'Registered Crimes Relative', 'GeregistreerdeMisdrijvenPer1000Inw_3': 'Registered CrimesPer1000Inw', 'TotaalOpgehelderdeMisdrijven_4': 'TotalClearedCrimes', 'OpgehelderdeMisdrijvenRelatief_5': 'ClearedCrimesRelative', 'RegistratiesVanVerdachten_6': 'RegistrationsofSuspects'})
        print('crime data successfully loaded')
        return data

    #Emmanuel
    def load_tourist_info(self):
        full_path = os.path.join(self.base_folder, 'data','raw','tourist_info.csv')
        data = pd.read_csv(full_path, sep=";")
        data = data.rename(columns={'WoonlandVanGasten': 'Residential Land Of Guests', 'RegioS': 'Municipalitycode', 'Perioden': 'Periods', 'Gasten_1': 'Guests', 'Overnachtingen_2': 'Overnights'})
        print('tourist info successfully loaded')
        return data

data_loader = DataLoader(base_folder=r'C:\\Users\\B.R\\Documents\\HvA\\Master DBB\AI for Business\\product3team2')
data = data_loader.load_funda_data_2020()
print(data.head())
print(data_2020.dtypes)