

import collections
import copy
from functools import partial
import json
import warnings

import numpy as np
import sklearn
import sklearn.preprocessing
from sklearn.utils import check_random_state

from lime.discretize import QuartileDiscretizer
from lime.discretize import DecileDiscretizer
from lime.discretize import EntropyDiscretizer
from lime.discretize import BaseDiscretizer
import math


def data_inverse(scaler, data_row, num_samples):
        """Generates a neighborhood around a prediction.
        For numerical features, perturb them by sampling from a Normal(0,1) and
        doing the inverse operation of mean-centering and scaling, according to
        the means and stds in the training data. For categorical features,
        perturb by sampling according to the training distribution, and making
        a binary feature that is 1 when the value is the same as the instance
        being explained.
        Args:
            data_row: 1d numpy array, corresponding to a row
            num_samples: size of the neighborhood to learn the linear model
        Returns:
            A tuple (data, inverse), where:
                data: dense num_samples * K matrix, where categorical features
                are encoded with either 0 (not equal to the corresponding value
                in data_row) or 1. The first row is the original instance.
                inverse: same as data, except the categorical features are not
                binary, but categorical (as the original data)
        """

        #print(scaler.scale_ )

        discretizer = None
        random_state = np.random.RandomState(0)
        sample_around_instance = True
        data = np.zeros((num_samples, data_row.shape[0]))
        categorical_features = []
        if discretizer is None:
            data = random_state.normal(
                    0, 1, num_samples * data_row.shape[0]).reshape(
                    num_samples, data_row.shape[0])
            if sample_around_instance:
                data = data * scaler.scale_ + data_row
            else:
                data = data * scaler.scale_ + scaler.mean_
            categorical_features = categorical_features
            first_row = data_row
        else:
            first_row = discretizer.discretize(data_row)
        data[0] = data_row.copy()
        inverse = data.copy()
        for column in categorical_features:
            values = feature_values[column]
            freqs = feature_frequencies[column]
            inverse_column = random_state.choice(values, size=num_samples,
                                                      replace=True, p=freqs)
            binary_column = np.array([1 if x == first_row[column]
                                      else 0 for x in inverse_column])
            binary_column[0] = 1
            inverse_column[0] = data[0, column]
            data[:, column] = binary_column
            inverse[:, column] = inverse_column
        if discretizer is not None:
            inverse[1:] = discretizer.undiscretize(inverse[1:])
        inverse[0] = data_row
        return data, inverse

import pandas as pd
df = pd.read_csv('uber_census_augmented.csv', encoding = "ISO-8859-1", engine='python')
df.drop('UserGroup',axis=1, inplace =True,) #removing the label column

categorical_features = df.select_dtypes(include=['object']).columns
print('Categorical features: ', categorical_features)
ohc_category = ['base']
df = pd.get_dummies(df, columns = ohc_category)
print('Columns: ', df.columns)

#converting the dataframe into numpy ndarray and fitting by scaler
array = df.to_numpy()
scaler = sklearn.preprocessing.StandardScaler(with_mean=False)
scaler.fit(array)
#print(array)

final_df = pd.DataFrame()

for index, row in df.iterrows():
    a = np.array(row.to_numpy())
    data, inverse = data_inverse(scaler, a, 10)
    df_aug = pd.DataFrame(data, 
             columns=['hour', 'lat', 'long', 'MedianIncomeByPlaceofBirth', 'MedianIncome','TotalPopulation', 'AvgPopulation', 'Population5M', 'Population45M', 'Population4M', 'Population35M', 'Population3M', 'base_B02512', 'base_B02598', 'base_B02617', 'base_B02682'])
 
    for index2, row2 in df_aug.iterrows():
        df_aug.at[index2, 'hour'] = math.floor( abs(row2['hour']) )
        if index2 == 0:
            b1 = row2['base_B02512']
            b2 = row2['base_B02598']
            b3 = row2['base_B02617']
            b4 = row2['base_B02682']
        else:
            df_aug.at[index2, 'base_B02512'] = b1
            df_aug.at[index2, 'base_B02598'] = b2
            df_aug.at[index2, 'base_B02617'] = b3
            df_aug.at[index2, 'base_B02682'] = b4

        


    print('Data: ', df_aug)

    final_df = pd.concat([final_df, df_aug], axis=0)

final_df.to_csv('uber_census_augmented_generated.csv', index=False)
