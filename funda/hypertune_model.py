import pandas as pd
import numpy as np
import itertools
from copy import deepcopy
import pickle
import os

# © Robin Kratschmayr
class Hypertuner(object):

    def __init__(self, estimator, tuning_params, run_folder):
        self.estimator = estimator
        self.tuning_params = tuning_params
        self.run_folder = run_folder

    def calculate_mean_cv_error(self, train_set, estimator_cv):
        # now perform cross validation fitting for each split
        splits = train_set['cv_split'].unique().tolist()
        splits.sort()
        cv_errors = []

        for i in splits:
            print(f'Crossvalidate Split {i} / {splits[-1]}')
            train_split = train_set.query(f"cv_split != {i}")
            X_train = train_split.drop(['sellingPrice', 'cv_split'],axis=1)
            y_train = train_split['sellingPrice']
            estimator_cv.fit(X=X_train, y = y_train)
            # evaluate the model on split 1
            test_obs = train_set.query(f"cv_split == {i}")
            X_test = test_obs.drop(['sellingPrice', 'cv_split'],axis=1)
            X_truth = test_obs['sellingPrice']
            y_pred = estimator_cv.predict(X_test)
            # calculate error measure on this fold for the estimator with the
            # given parameters
            rmse = np.sqrt(np.sum(np.square(X_truth - y_pred))/X_test.shape[0])
            cv_errors.append(rmse)
        return sum(cv_errors)/len(cv_errors), estimator_cv

    def tune_model(self, train_set):
        '''Perform the hypertuning of the estimator on the train set
        for all the combinations of the hyperparameters
        '''
        parameter_combos = []
        parameter_combos_dicts = []
        for a in itertools.product(*self.tuning_params.values()):
            parameter_combos.append(a)
        for i in parameter_combos:
            d = {}
            for j in range(len(i)):
                d[list(self.tuning_params.keys())[j]] = i[j]
            parameter_combos_dicts.append(d)

        #set arbitrary high number for best_mode_mse that will be overwritten after first run
        #in case the first run mse is worse than this number, the mdel is so bad that it does not deserve to be saved. 
        # An error would be thrown and the params in the conf.json have to be adapted
        best_model_mse = 10000000000
        best_model_params = ''
        best_model_name = ''

        #hypertune model for all combos
        for d in parameter_combos_dicts:
            estimator_cv = deepcopy(self.estimator)
            estimator_cv = estimator_cv.set_params(**d)
            mean_cv_error, trained_estimator = self.calculate_mean_cv_error(train_set, estimator_cv)
            print(f"Best parameters: {d}, RMSE: {mean_cv_error}")
            # save best model params
            if mean_cv_error < best_model_mse:
                best_model_params = d
                best_model_mse = mean_cv_error

        #train estiamtor on full train set with best parmeters and save it to disk
        estimator_final = deepcopy(self.estimator)
        estimator_final = estimator_final.set_params(**best_model_params)
        X_train = train_set.drop(['sellingPrice', 'cv_split'],axis=1)
        y_train = train_set['sellingPrice']
        estimator_final.fit(X=X_train, y = y_train)
        pickle.dump(estimator_final, open(os.path.join(self.run_folder, 'models' , f'Model_{best_model_params}_RMSE:_{best_model_mse}.sav' ), 'wb'))

        return estimator_final, best_model_mse, best_model_params