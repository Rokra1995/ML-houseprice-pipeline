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
    @staticmethod
    def funda_data(data):

        return data

    # © Emmanuel Owusu Annim
    @staticmethod
    def cbs_data(data):

        return data

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
    

