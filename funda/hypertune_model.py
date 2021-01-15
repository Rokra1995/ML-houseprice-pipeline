import pandas as pd
import numpy as np
import itertools
from copy import deepcopy
import pickle
import os

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

        tested_models = []
        best_model_mse = 1000000000
        best_model_params = ''
        best_model_name = ''

        for d in parameter_combos_dicts:
            print('testing combo: ', d)
            estimator_cv = deepcopy(self.estimator)
            estimator_cv = estimator_cv.set_params(**d)
            mean_cv_error, trained_estimator = self.calculate_mean_cv_error(train_set, estimator_cv)
            tested_models.append([d,mean_cv_error])
            # saving best model to disk
            if mean_cv_error < best_model_mse:
                filename = 'Best_model.sav'
                pickle.dump(trained_estimator, open(os.path.join(self.run_folder, 'models' , 'Best_model.sav' ), 'wb'))
                best_model_params = d
                best_model_mse = mean_cv_error
        print(tested_models)

        # Renaming the best saved model with params and mse
        string = 'Best_model'
        for k,v in best_model_params.items():
            string = string + '_'+k+':'+str(v)

        string = string + 'MSE:' + str(best_model_mse)
        string = string + '.sav'

        os.rename(os.path.join(self.run_folder, 'models' , 'Best_model.sav' ),os.path.join(self.run_folder, 'models' , string ))
        best_model_name = string

        return tested_models, best_model_mse, best_model_params, best_model_name