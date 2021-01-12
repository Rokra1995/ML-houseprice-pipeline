import pandas as pd
import numpy as np

# Robin Kratschmayr
class DataPartitioner(object):
    '''Class to partition data into train and test,
    and to partition test into 5-fold cross validation splits.
    '''
    def __init__(self, perc_test = 0.2, train_cv_splits = 5, seed = 1234):
        self.perc_test = perc_test
        self.train_cv_splits = train_cv_splits
        self.seed = seed

    def partition_data(self, data):
        obs = data.copy()
        obs_test = obs.sample(frac=self.perc_test, random_state = self.seed).copy()
        obs_test = obs_test.assign(test = True).assign(cv_split=np.nan)

        obs_train = (
        obs.merge(obs_test, how = 'left', indicator = True)
        .query("_merge == 'left_only'")
        .drop('_merge', axis=1)
        .assign(test=False))
        cv_splits = np.random.randint(1, self.train_cv_splits + 1, obs_train.shape[0])
        obs_train = obs_train.assign(cv_split = cv_splits)
        final_obs = pd.concat([obs_test, obs_train]).reset_index(drop=True)
        return final_obs