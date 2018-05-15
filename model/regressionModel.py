# coding=utf-8
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn import linear_model
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error
from sklearn.cross_validation import train_test_split
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error

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

# 准备特征和标签，特征归一化
data_X = data[:, :-1]
data_Y = data[:, -1]
data_x_norm = preprocessing.normalize(data_X, norm='l2', axis=0)

# 模型选择
reg = linear_model.Ridge(alpha=.5)
#reg = linear_model.LinearRegression()

# 交叉验证
n_splits = 5
kf = KFold(n_splits=n_splits)
MSE_SUM = 0.0
MAE_SUM = 0.0
for train_index, test_index in kf.split(data_x_norm):
    # print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = data_x_norm[train_index], data_x_norm[test_index]
    y_train, y_test = data_Y[train_index], data_Y[test_index]
    reg.fit(X_train, y_train)
    y_pred = reg.predict(X_test)
    MSE_SUM += mean_squared_error(y_test, y_pred)
    MAE_SUM += mean_absolute_error(y_test, y_pred)

    # print r2_score(y_test, y_pred)

MAE = MAE_SUM / n_splits
MSE = MSE_SUM / n_splits
print "MSE: " + str(MSE)
print "MAE: " + str(MAE)

