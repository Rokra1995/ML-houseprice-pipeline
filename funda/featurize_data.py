import pandas as pd
import numpy as np

class Featurizer(object):

    # © Felicia Betten
    @staticmethod
    def featurize_funda_data(data):

        return data

    # © Emmanuel Owusu Annim
    @staticmethod
    def featurize_cbs_data(data):

        return data

    # © Robin Kratschmayr
    @staticmethod
    def featurize_broke_info(broker_info):
        broker_features = broker_info.drop(columns=['zipcode_broker','description_broker','url'])
        return broker_features

    # © to be discussed
    @staticmethod
    def combine_featurized_data(funda,cbs,brokers):
        pass

