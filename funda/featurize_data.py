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

    # © Robin Kratschmayr
    @staticmethod
    def combine_featurized_data(funda,cbs,brokers):
        # merging columns need to be changed
        data = funda.merge(cbs, how="left", left_on="Municipality_code", right_on="Municipality_code")
        data = data.merge(cbs, how="left", left_on="district_code", right_on="district_code", suffixes=['GM','WK'])
        data = data.merge(brokers, how="left", left_on="Sales_Agent", right_on="Broker_name")
        data = data.merge(brokers, how="left", left_on="buy_Agent", right_on="Broker_name", suffixes=['Sale','Buy'])
        return data

