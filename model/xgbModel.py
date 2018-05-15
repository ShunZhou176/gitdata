# coding=utf-8
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error
from sklearn.cross_validation import train_test_split
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
import xgboost as xgb

df = pd.read_csv('/Users/JDN/Desktop/allfeature_nonull.csv')
df = df.replace('None', 0)
df = df.replace('NaN', 0)
df = df[['commits_year_ratio_min',
         'communityhealth',
         'forks_year_incre_kurt',
         'stargazers_month_ratio_skew',
         'forks_month_ratio_skew',
         'active_ratio',
         'tags_NUMS',
         'commits_month_ratio_mean',
         'forks_year_incre_skew',
         'commits_month_ratio_std',
         'stargazers_year_incre_min', 'rate']]
data = df.values

# 准备特征和标签
data_X = data[:, :-1]
data_Y = data[:, -1]

n_splits = 10
kf = KFold(n_splits=n_splits)
MSE_SUM = 0.0
MAE_SUM = 0.0
param = {'max_depth': 2, 'eta': 1, 'silent': 1, 'objective': 'reg:linear'}
num_round = 2
for train_index, test_index in kf.split(data_X):
    # print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = data_X[train_index], data_X[test_index]
    y_train, y_test = data_Y[train_index], data_Y[test_index]
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dtest = xgb.DMatrix(X_test, label=y_test)
    bst = xgb.train(param, dtrain, num_round)
    # make prediction
    preds = bst.predict(dtest)
    MSE_SUM += mean_squared_error(y_test, preds)
    MAE_SUM += mean_absolute_error(y_test, preds)

MAE = MAE_SUM / n_splits
MSE = MSE_SUM / n_splits
print "MSE: " + str(MSE)
print "MAE: " + str(MAE)

