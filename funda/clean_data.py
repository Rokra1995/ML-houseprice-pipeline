#Baris
def cleaned_funda_2018(data):
    #Renaming the columns to english
    funda_2018 = data
    funda_2018 = funda_2018.fillna(0).rename(columns={'publicatieDatum':'publicationDate','postcode':'zipcode', 'koopPrijs':'sellingPrice',\
        'volledigeOmschrijving':'fullDescription','soortWoning':'houseType','categorieObject':'categoryObject', 'bouwjaar':'yearOfBuilding', \
        'indTuin':'garden','perceelOppervlakte':'parcelSurface','aantalKamers':'numberRooms','aantalBadkamers':'numberBathrooms',   'energielabelKlasse':'energylabelClass',\
        'oppervlakte':'surface','datum_ondertekening':'sellingDate'}).drop(['globalId', 'globalId.1','kantoor_naam_MD5hash'], axis=1)

    #Changing dataypes for publication date and selling date
    funda_2018['publicationDate'] = pd.to_datetime(funda_2018['publicationDate'])
    funda_2018['sellingDate'] = pd.to_datetime(funda_2018['sellingDate'])
    
    
    #HOUSETYPE AND CATEGORYOBJECT: SEPERATE THE VARIABALES WITH COMMA'S AND REMOVE THE BRACKETS
git     funda_2018['houseType'] = funda_2018['houseType'].str.replace('<', "").str.replace('{', "").str.replace('}', "").str.replace('>', "")
    funda_2018['categoryObject'] = funda_2018['categoryObject'].str.replace('<', "").str.replace('{', "").str.replace('}', "").str.replace('>', "")
    funda_2018['fullDescription'] = funda_2018['fullDescription'].str.replace("\n", "")

             
    #Calculation of sellingtime and adding the column
    funda_2018['sellingTime'] = pd.to_datetime(funda_2018['sellingDate']) - pd.to_datetime(funda_2018['publicationDate'])
    funda_2018['sellingTime'] = funda_2018['sellingTime'].apply(lambda x: int(x.days))

    #Replace the 0 in Parcelsruface with NaN
    funda_2018['parcelSurface'] = funda_2018['parcelSurface'].replace(0.0, np.nan)
    
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

    
    funda_2018['yearOfBuilding'] = funda_2018['yearOfBuilding'].apply(lambda date: mean_yearofBuilding_funda_2018(date))
    
    datatypes_funda_2018 = funda_2018.dtypes

    return funda_2018