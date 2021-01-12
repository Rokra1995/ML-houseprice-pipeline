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
        full_path = os.path.join(self.base_folder, 'data/raw/crime_data.csv')
        crime_data = pd.read_csv(full_path, sep=";")
        crime_data = crime_data.drop(['ID', 'SoortMisdrijf', 'Perioden'], axis=1)
        crime_data = crime_data.rename(columns={'SoortMisdrijf': 'CrimeType', 'RegioS': 'Municipalitycode', 'Perioden': 'Periods', 'TotaalGeregistreerdeMisdrijven_1': 'Total Registered Crimes', 'GeregistreerdeMisdrijvenRelatief_2': 'Registered Crimes Relative', 'GeregistreerdeMisdrijvenPer1000Inw_3': 'Registered CrimesPer1000Inw', 'TotaalOpgehelderdeMisdrijven_4': 'TotalClearedCrimes', 'OpgehelderdeMisdrijvenRelatief_5': 'ClearedCrimesRelative', 'RegistratiesVanVerdachten_6': 'RegistrationsofSuspects'})
        print('ID, SoortMisdrijf & Perioden successfully dropped')
        crime_data = crime_data.replace(0.0, np.nan)
        crime_data = crime_data.replace(0, np.nan)
        crime_data = crime_data.replace("       .", np.nan)
        crime_data = crime_data.replace("         .", np.nan)
        print('All the zero values are replaced with NaN')
        type_dict = {'Municipalitycode': 'string',
                'Registered CrimesPer1000Inw':'float',
                }

        for k,v in type_dict.items():
                crime_data = crime_data.astype({k: v})

        full_path = os.path.join(self.base_folder, 'data/raw/tourist_info.csv')
        tourist_info = pd.read_csv(full_path, sep=";")
        tourist_info = tourist_info.rename(columns={'WoonlandVanGasten': 'Residential Land Of Guests', 'RegioS': 'Municipalitycode', 'Perioden': 'Periods', 'Gasten_1': 'Guests', 'Overnachtingen_2': 'Overnights'})
        tourist_info = tourist_info.drop(['ID', 'Residential Land Of Guests', 'Periods'], axis=1)
        print('ID, Residential Land Of Guests & Periods successfully dropped')
        tourist_info = tourist_info.replace(0.0, np.nan)
        tourist_info = tourist_info.replace(0, np.nan)
        print('All the zero values are replaced with NaN')
        type_dict = {'Municipalitycode': 'string',
                'Guests':'float',
                }

        for k,v in type_dict.items():
                tourist_info = tourist_info.astype({k: v})

        full_path = os.path.join(self.base_folder, 'data', 'raw', 'CBS_data.csv')
        cbs_data_old = pd.read_csv(full_path, sep=";")
        cbs_data_old = cbs_data_old.drop(['ID', 'Gemeentenaam_1', 'Codering_3'], axis=1)
        cbs_data_old = cbs_data_old.rename(columns={'WijkenEnBuurten':'Municipalitycode','Gemeentenaam_1':'NameOfMunicipality','Mannen_6':'NumberOfMen',
'Vrouwen_7':'NumberOfWomen','k_0Tot15Jaar_8':'AgeFrom0to15years','k_15Tot25Jaar_9':'AgeFrom15to25years',
'k_25Tot45Jaar_10' : 'AgeFrom25to45years','k_45Tot65Jaar_11' : 'AgeFrom45to65years','k_65JaarOfOuder_12' : 'AgeFrom65AndOlder',
'Bevolkingsdichtheid_33' : 'PopulationDensity','Woningvoorraad_34' : 'HousingStock','PercentageBewoond_38' : 'PercentageInhabited',
'PercentageOnbewoond_39' : 'PercentageUninhabited','Koopwoningen_40' : 'OwnerOccupiedHouses','HuurwoningenTotaal_41' : 'RentalHouses',
'BouwjaarVoor2000_45' : 'ConstructionYearBefore2000','BouwjaarVanaf2000_46' : 'ConstructionYearAfter2000',
'GemiddeldInkomenPerInwoner_66' : 'AverageIncomePerCitizen','MeestVoorkomendePostcode_103' : 'MostCommonPostalCode','Dekkingspercentage_104' : 'CoveragePercentage'})
        print('ID, Gemeentenaam_1 & Codering_3 succesfully dropped')
        cbs_data_old = cbs_data_old.replace("       .", np.nan)
        cbs_data_old = cbs_data_old.replace("         .", np.nan)
        type_dict = {'Municipalitycode': 'string',
                'PopulationDensity':'float',
                'PercentageInhabited':'float',
                'PercentageUninhabited':'float',
                'OwnerOccupiedHouses':'float',
                'RentalHouses':'float',
                'ConstructionYearBefore2000':'float',
                'ConstructionYearAfter2000':'float',
                'AverageIncomePerCitizen':'float',
                'MostCommonPostalCode':'string',
                'CoveragePercentage':'float',
                }

        for k,v in type_dict.items():
                cbs_data_old = cbs_data_old.astype({k: v})

        print("Counting the NaN values in the columns Men, Women and their Ages\n")
        print("Number of null values in column NumberOfMen : " + 
        str(cbs_data_old['NumberOfMen'].isnull().sum())) 
        print("Number of null values in column NumberOfWomen: " + 
        str(cbs_data_old['NumberOfWomen'].isnull().sum()))
        print("Number of null values in column AgeFrom0to15years : " + 
        str(cbs_data_old['AgeFrom0to15years'].isnull().sum())) 
        print("Number of null values in column AgeFrom15to25years : " + 
        str(cbs_data_old['AgeFrom15to25years'].isnull().sum())) 
        print("Number of null values in column AgeFrom25to45years: " + 
        str(cbs_data_old['AgeFrom25to45years'].isnull().sum()))
        print("Number of null values in column AgeFrom45to65years : " + 
        str(cbs_data_old['AgeFrom45to65years'].isnull().sum()))
        print("Number of null values in column AgeFrom65AndOlder : " + 
        str(cbs_data_old['AgeFrom65AndOlder'].isnull().sum()))  

        
        print("Counting all the NaN values in all the columns for the Crime Data File")
        display(crime_data.isnull().sum())
        print("Counting all the NaN values in all the columns for the Tourist Info File")
        display(tourist_info.isnull().sum()) 
        print("Counting all the NaN values in all the columns for the CBS File")
        display(cbs_data_old.isnull().sum()) 

        print("Check Data Types of CrimeData, TouristInfo & CSB")
        crime_data.dtypes
        tourist_info.dtypes
        cbs_data_old.dtypes

        print("Check the MEAN of all the columns of the CBS File")
        cbs_data_old.mean()

        #Fill NAN with Mean & Print new data set called cbs_data
        cbs_data = cbs_data_old.fillna(cbs_data_old.mean())
        print("The NaN Values have been replaced with the mean of the columns")
        cbs_data

        print("Confirming that all the NAN values are gone")
        display(cbs_data.isnull().sum()) 
        
        #Merge TouristData & CrimeData together on key 'Municipalitycode'
        merge1 = (pd.merge(crime_data, tourist_info, on='Municipalitycode'))

        #Merge CBS Data with Merge1 and make a complete df of all the data
        all_data = cbs_data.merge(merge1, on='Municipalitycode', how='inner').sort_values(['Municipalitycode'])

        print(all_data)

        return crime_data, tourist_info, cbs_data_old

    # © Robin Kratschmayr
    @staticmethod
    def featurize_broke_info(broker_info):
        broker_features = broker_info.drop(columns=['zipcode_broker','description_broker','url'])
        return broker_features

    # © to be discussed
    @staticmethod
    def combine_featurized_data(funda,cbs,brokers):
        pass

