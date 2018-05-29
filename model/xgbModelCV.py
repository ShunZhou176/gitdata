# coding=utf-8
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error
from sklearn.cross_validation import train_test_split
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import ShuffleSplit
import xgboost as xgb

df = pd.read_csv('/Users/JDN/Desktop/newfeature.csv')
df = df.replace('None', 0)
df = df.replace('NaN', 0)
# df = df[['forks_month_ratio_skew',
#          'communityhealth',
#          'stargazers',
#          'commits_year_ratio_min',
#          'stargazers_month_ratio_skew',
#          'issues_quart_ratio_min',
#          'pulls_month_ratio_skew',
#          'tags_month_nums_skew',
#          'forks_quart_incre_skew',
#          'tags_quart_nums_skew',
#          'stargazers_year_incre_skew',
#          'rate']]

df = df[['comments_year_ratio_min',
         'comments_year_ratio_median',
         'issues_month_nums_skew',
         'stargazers_quart_incre_skew',
         'stargazers_year_incre_skew',
         'tags_month_incre_kurt',
         'tags_quart_incre_kurt',
         'tags_year_nums_kurt',
         'tags_quart_nums_kurt',
         'tags_month_nums_kurt',
         'tags_year_nums_skew',
         'tags_quart_nums_skew',
         'forks_quart_incre_skew',
         'tags_month_nums_skew',
         'forks_month_ratio_skew',
         'communityhealth',
         'stargazers',
         'commits_year_ratio_min',
         'stargazers_month_ratio_skew',
         'issues_quart_ratio_min',
         'pulls_month_ratio_skew',
         'forks_year_ratio_median',
         'forks_quart_incre_kurt',
         'issues_month_ratio_skew',
         'communityimpact',
         'pulls_quart_ratio_skew',
         'stargazers_quart_incre_kurt',
         'forks_month_ratio_mean',
         'tags_month_incre_skew',
         'subscribers',
         'stargazers_quart_ratio_min',
         'forks_quart_ratio_median','rate']]

data = df.values

# 准备特征和标签
data_X = data[:, :-1]
data_Y = data[:, -1]

n_splits = 10
ss = ShuffleSplit(n_splits=n_splits, test_size=0.1, random_state=5)
MSE_SUM = 0.0
MAE_SUM = 0.0
param = {'max_depth': 2, 'eta': 1, 'silent': 1, 'objective': 'reg:linear'}
num_round = 2
for train_index, test_index in ss.split(data_X):
    print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = data_X[train_index], data_X[test_index]
    y_train, y_test = data_Y[train_index], data_Y[test_index]
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dtest = xgb.DMatrix(X_test, label=y_test)
    bst = xgb.train(param, dtrain, num_round)
    # make prediction
    preds = bst.predict(dtest)
    MSE_SUM += mean_squared_error(y_test, preds)
    MAE_SUM += mean_absolute_error(y_test, preds)
    print mean_absolute_error(y_test, preds)

MAE = MAE_SUM / n_splits
MSE = MSE_SUM / n_splits
print "MSE: " + str(MSE)
print "MAE: " + str(MAE)
