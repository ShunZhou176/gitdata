# coding=utf-8
from sklearn import svm
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.metrics import classification_report
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn import linear_model
import numpy as np


df = pd.read_csv('/Users/JDN/Desktop/newfeature.csv')
df = df.replace('None', 0)
df = df.replace('NaN', 0)
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
         'forks_quart_ratio_median',
         'rate']]
data = df.values
binary = lambda x : 1 if x > 4 else 0
classification = df['rate'].map(binary)
data_Y = classification.values
data_X = data[:, 1:-1]
# condition = data_Y == 1
# print len(np.extract(condition, data_Y))


#模型选择
#clf = svm.SVC()
clf = NearestCentroid()

# 交叉验证
n_splits = 5
kf = KFold(n_splits=n_splits)
for train_index, test_index in kf.split(data_X):
    # print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = data_X[train_index], data_X[test_index]
    y_train, y_test = data_Y[train_index], data_Y[test_index]
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred))




