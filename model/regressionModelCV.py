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
from sklearn.model_selection import ShuffleSplit

df = pd.read_csv('/Users/JDN/Desktop/feature.csv')
df = df.replace('None', 0)
df = df.replace('NaN', 0)
# df = df[['commits_year_ratio_min',
#          'communityhealth',
#          'forks_year_incre_kurt',
#          'stargazers_month_ratio_skew',
#          'forks_month_ratio_skew',
#          'active_ratio',
#          'tags_NUMS',
#          'commits_month_ratio_mean',
#          'forks_year_incre_skew',
#          'commits_month_ratio_std',
#          'stargazers_year_incre_min', 'rate']]
#
# df = df[['comments_year_ratio_min',
#          'comments_year_ratio_median',
#          'issues_month_nums_skew',
#          'stargazers_quart_incre_skew',
#          'stargazers_year_incre_skew',
#          'tags_month_incre_kurt',
#          'tags_quart_incre_kurt',
#          'tags_year_nums_kurt',
#          'tags_quart_nums_kurt',
#          'tags_month_nums_kurt',
#          'tags_year_nums_skew',
#          'tags_quart_nums_skew',
#          'forks_quart_incre_skew',
#          'tags_month_nums_skew',
#          'forks_month_ratio_skew',
#          'communityhealth',
#          'stargazers',
#          'commits_year_ratio_min',
#          'stargazers_month_ratio_skew',
#          'issues_quart_ratio_min',
#          'pulls_month_ratio_skew',
#          'forks_year_ratio_median',
#          'forks_quart_incre_kurt',
#          'issues_month_ratio_skew',
#          'communityimpact',
#          'pulls_quart_ratio_skew',
#          'stargazers_quart_incre_kurt',
#          'forks_month_ratio_mean',
#          'tags_month_incre_skew',
#          'subscribers',
#          'stargazers_quart_ratio_min',
#          'forks_quart_ratio_median','rate']]
#
df = df[['forks_month_ratio_skew',
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
         'forks_quart_ratio_median',
         'commits_quart_ratio_min',
         'forks_year_incre_kurt',
         'stargazers_year_nums_max',
         'tags_quart_nums_median',
         'tags_quart_incre_skew',
         'stargazers_year_incre_kurt',
         'pulls_quart_ratio_min',
         'commits_year_ratio_median',
         'forks_quart_ratio_min',
         'stargazers_month_ratio_kurt',
         'tags_month_nums_median',
         'active_ratio',
         'tags_month_ratio_std',
         'forks_month_ratio_kurt',
         'forks_quart_ratio_kurt',
         'stargazers_year_nums_mean',
         'forks_month_ratio_min',
         'tags_year_nums_median',
         'stargazers_year_incre_min',
         'commits_month_nums_skew',
         'commits_quart_nums_skew',
         'forks_year_incre_skew',
         'commits_year_nums_skew',
         'comments_year_ratio_min',
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
         'tags_month_nums_skew','rate']]

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
ss = ShuffleSplit(n_splits=n_splits, test_size=0.1,random_state=5)
MSE_SUM = 0.0
MAE_SUM = 0.0
for train_index, test_index in ss.split(data_x_norm):
    print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = data_x_norm[train_index], data_x_norm[test_index]
    y_train, y_test = data_Y[train_index], data_Y[test_index]
    reg.fit(X_train, y_train)
    y_pred = reg.predict(X_test)
    MSE_SUM += mean_squared_error(y_test, y_pred)
    MAE_SUM += mean_absolute_error(y_test, y_pred)


MAE = MAE_SUM / n_splits
MSE = MSE_SUM / n_splits
print "MSE: " + str(MSE)
print "MAE: " + str(MAE)



