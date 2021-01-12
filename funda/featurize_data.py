'''This module contains a class with features
'''

import pandas as pd
import numpy as np
import nltk
import re
try: 
    from nltk import word_tokenize, pos_tag
    from nltk.sentiment.util import mark_negation
    from nltk.corpus import wordnet as wn
    from nltk.corpus import sentiwordnet as swn
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer 
except Exception as e:
    print('Failed during package load. with error: ', e)
    print('Attempting to download the required NLP modules...')
    nltk.download('wordnet')
    nltk.download('stopwords')
    nltk.download('sentiwordnet')
    from nltk import word_tokenize, pos_tag
    from nltk.sentiment.util import mark_negation
    from nltk.corpus import wordnet as wn
    from nltk.corpus import sentiwordnet as swn
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    


class Featurizer(object):
    
    def __init__(self):
        self.discard_tokens = stopwords.words('dutch')
        self.lemmatizer = WordNetLemmatizer()
        #still under development
        #self.house_features = ['pool', 'zonnepaneel', 'gerenoveerd']
    
    # Credits go to Emmas Code example
    def sentiment_score(text):
        #### Sentiment WITH pos tags and negation, WITHOUT skipping incompatible tags
        sentence = text
        tokens = word_tokenize(sentence)
        tokens_neg = mark_negation(tokens)
        tagged = pos_tag(tokens_neg)

        def penn_to_wn(tag):
            #Convert between the PennTreebank tags to simple Wordnet tags
            if tag.startswith('J'):
                return wn.ADJ
            elif tag.startswith('N'):
                return wn.NOUN
            elif tag.startswith('R'):
                return wn.ADV
            elif tag.startswith('V'):
                return wn.VERB
            return None

        sentiment = 0.0
        for word, tag in tagged:
            # Check for negation
            neg_coef = 1
            if re.search("_NEG$", word):
                neg_coef = -1
                word = re.sub("_NEG$", "", word)
            # Convert pos tag
            tag_converted = penn_to_wn(tag)
            # Find Lemma
            if tag_converted not in (wn.NOUN, wn.ADJ, wn.ADV, wn.VERB):
                lemma = self.lemmatizer.lemmatize(word)
            else:
                lemma = self.lemmatizer.lemmatize(word, pos=tag_converted)   
            if not lemma:
                continue

            # Find word sense
            if tag_converted not in (wn.NOUN, wn.ADJ, wn.ADV, wn.VERB):
                synsets = wn.synsets(lemma)
            else:
                synsets = wn.synsets(lemma, pos=tag_converted)
            if not synsets:
                continue

            # Take the first sense, the most common
            synset = synsets[0]
            # Associate sentiment with word sense
            swn_synset = swn.senti_synset(synset.name())
            # Calculate sentiment, and add it to the sentence score.
            sentiment += neg_coef*(swn_synset.pos_score() - swn_synset.neg_score())

        return sentiment

    # © Felicia Betten
    def funda_data(self, funda_2018_cleaned, zipcode_data_cleaned, brt_data_cleaned, funda_2020_cleaned):
        # create column with publication day, month and year
        funda_2018_cleaned['publicationDay'] = pd.DatetimeIndex(funda_2018_cleaned['publicationDate']).day
        funda_2018_cleaned['publicationMonth'] = pd.DatetimeIndex(funda_2018_cleaned['publicationDate']).month
        funda_2018_cleaned['publicationYear'] = pd.DatetimeIndex(funda_2018_cleaned['publicationDate']).year
        # dummy code categoryObject & energylabelClass
        funda_2018_cleaned = pd.get_dummies(data=funda_2018_cleaned, columns=['categoryObject', 'energylabelClass'])
        # drop columns publicationDate, sellingPrice, sellingTime and sellingDate
        funda_2018_cleaned = funda_2018_cleaned.drop(columns=['publicationDate', 'sellingPrice', 'sellingTime', 'sellingDate'])
        funda_2018_cleaned['houseType'] = funda_2018_cleaned['houseType'].replace({'2-onder-1-kapwoning':'semi-detachedresidentialproperty', 'bel-etage':'Ground-floorapartment', 'beneden+bovenwoning':'Ground-floor+upstairsapartment', 'benedenwoning':'Residentialpropertywithsharedstreetentrance', 'bovenwoning':'Upstairsapartment', 'bungalow':'Bungalow', 'dubbelbenedenhuis':'Doubleground-floorapartment', 'eengezinswoning':'Single-familyhome', 'galerijflat':'Galleriedapartment', 'geschakelde2-onder-1-kapwoning':'linkedsemi-detachedresidentialproperty', 'grachtenpand':'Propertyalongsidecanal', 'halfvrijstaandewoning':'detachedresidentialproperty', 'hoekwoning':'cornerhouse', 'penthouse':'Penthouse', 'landgoed':'Countryestate', 'landhuis':'Countryhouse', 'maisonnette':'Maisonnette', 'stacaravan':'Mobilehome', 'semi-bungalow':'semi-detachedresidentialproperty', 'verspringend':'staggered', 'studentenkamer':'Studentroom', 'tussenverdieping':'Mezzanine', 'villa':'Villa', 'vrijstaandewoning':'Desirableresidence/villa', 'woonboerderij':'Convertedfarmhouse', 'woonboot':'Houseboat', 'OpenPortiek':'Apartmentwithsharedstreetentrance', 'OpenPortiek2':'Apartmentwithsharedstreetentrance', 'portiekflat':'Apartmentwithsharedstreetentrance', 'portiekwoning':'Apartmentwithsharedstreetentrance', 'dubbelbovenhuis':'doublehouse', 'appartement':'Apartmentwithsharedstreetentrance', 'bedrijfs-ofdienstwoning':'companyresidenceofficialresidence', 'corridorflat':'Apartmentwithsharedstreetentrance', 'dijkwoning':'dykehouse', 'drive-inwoning':'drive-in house', 'eindwoning':'Apartmentwithsharedstreetentrance', 'geschakeldewoning':'semi-detachedresidentialproperty', 'herenhuis':'mansion', 'hofjeswoning':'Countryhouse', 'kwadrantwoning':'quadranthouse', 'paalwoning':'stilthouse'}, 'patiowoning':'patiohouse', 'split-levelwoning':'split-levelhouse', 'tussenwoning':'rowhouse', 'verzorgingsflat':'nursing-home', 'waterwoning':'waterhouse', 'wind/watermolen':'wind/watermill', regex=True)

        # combine csv files funda_2018 and pc6-gwb2020 (postcodes), join them on zipcode
        funda_zipcode_df = funda_2018_cleaned.join(zipcode_data_cleaned.set_index('zipcode'), on='zipcode')
        # combine csv files funda_2018, pc6-gwb2020 and brt, join them on NeighborhoodCode
        # right: use only keys from right frame, similar to a SQL right outer join; preserve key order.
        funda_zipcode_brt_df = funda_zipcode_df.merge(brt_data_cleaned, on='NeighborhoodCode', how='right')
        # drop columns NeighborhoodCode, DistrictCode_x, Municipalitycode_x and exclude _y from columns names
        funda_zipcode_brt_df = funda_zipcode_brt_df.drop(columns=['NeighborhoodCode', 'DistrictCode_x', 'Municipalitycode_x']).rename(columns={'Municipalitycode_y':'Municipalitycode', 'DistrictCode_y':'DistrictCode'})

        # create new dataframe with houseTypes dummy codes
        houseTypes_df_funda_2018 = funda_2018_cleaned['houseType'].str.get_dummies(sep=",")
        # join houseType_df with funda_2018
        joined_df = funda_2018_cleaned.join(houseTypes_df_funda_2018, how='right').drop(axis=1, columns='houseType')
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

        # create column with publication day, month and year
        funda_2020_cleaned['publicationDay'] = pd.DatetimeIndex(funda_2020_cleaned['publicationDate']).day
        funda_2020_cleaned['publicationMonth'] = pd.DatetimeIndex(funda_2020_cleaned['publicationDate']).month
        funda_2020_cleaned['publicationYear'] = pd.DatetimeIndex(funda_2020_cleaned['publicationDate']).year
        # drop columns publicationDate, sellingPrice, Asking_Price_M2, Facilities, description_garden, sellingDate, sellingtime and url
        # and rename columns to the same names in funda_2018
        funda_2020_cleaned = funda_2020_cleaned.drop(columns=['publicationDate', 'sellingPrice', 'Asking_Price_M2', 'Facilities', 'description_garden', 'sellingDate', 'sellingtime', 'url']).rename(columns={'fulldescription':'fullDescription', 'yearofbuilding':'yearofbuilding', 'garden_binary':'garden', 'housetype':'houseType', 'parcelsurface':'parcelSurface', 'energylabelclass':'energylabelClass','numberrooms':'numberRooms', 'numberbathrooms':'numberBathrooms'})
        # remove the brackets and its content for housetype
        funda_2020_cleaned['houseType'] = funda_2020_cleaned['houseType'].str.replace(r"\(.*\)","").str.lstrip().str.replace('\r\n', '')
        # dummy code energylabelClass
        funda_2020_cleaned = pd.get_dummies(data=funda_2020_cleaned, columns=['energylabelClass'])
        # replace NaN sales_agent and buying_agent with -1
        funda_2020_cleaned['sales_agent'] = funda_2020_cleaned['sales_agent'].fillna(-1)
        funda_2020_cleaned['buying_agent'] = funda_2020_cleaned['buying_agent'].fillna(-1)
        # dummy code sales_agent and buying_agent
        funda_2020_cleaned = pd.get_dummies(data=funda_2020_cleaned, columns=['sales_agent', 'buying_agent'])    

        # merge funda_zipcode_brt_df with funda_2020_cleaned
        # funda_2020 to funda_zipcode_brt_df? 

        return all_data

    # © Emmanuel Owusu Annim
    @staticmethod
    def cbs_data(data):
        #Here I fill NAN values with the MEAN and I printed a new data set called cbs_data
        cbs_data = cbs_data_old.fillna(cbs_data_old())
        cbs_data['Municipalitycode'] = cbs_data['Municipalitycode'].str.strip()

        #Here I merged the other data sets TouristData & Crimedata together on the key 'Municipalitycode'
        merge1 = (pd.merge(crime_data, tourist_info, on='Municipalitycode'))

        #Here I merged the dataset cbs_data with Merge1 and make a complete datasett of all the data
        all_data = cbs_data.merge(merge1, on='Municipalitycode', how='left').sort_values(['Municipalitycode']).fillna(-1)
        return all_data

   # © Robin Kratschmayr
    @staticmethod
    def broker_info(broker_info):
        broker_features = broker_info.drop(columns=['zipcode_broker','description_broker','url'])
        return broker_features

    # © Robin Kratschmayr
    @staticmethod
    def combine_featurized_data(funda,cbs,brokers):
        # merging columns need to be changed
        data = funda.merge(cbs, how="left", left_on="Municipality_code", right_on="Municipality_code")
        data = data.merge(cbs, how="left", left_on="district_code", right_on="district_code", suffixes=['GM','WK'])
        data = data.merge(brokers, how="left", left_on="Sales_Agent", right_on="Broker_name")
        data = data.merge(brokers, how="left", left_on="buy_Agent", right_on="Broker_name", suffixes=['Sale','Buy'])
        return data
