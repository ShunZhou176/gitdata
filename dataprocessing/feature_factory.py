import numpy as np
import pandas as pd
import os
file_names = [
 'comments_month.txt',
 'comments_quart.txt',
 'comments_year.txt',
 'commits_month.txt',
 'commits_quart.txt',
 'commits_year.txt',
 'forks_month.txt',
 'forks_quart.txt',
 'forks_year.txt',
 'issues_month.txt',
 'issues_quart.txt',
 'issues_year.txt',
 'pulls_month.txt',
 'pulls_quart.txt',
 'pulls_year.txt',
 'stargazers_month.txt',
 'stargazers_quart.txt',
 'stargazers_year.txt',
 'tags_month.txt',
 'tags_quart.txt',
 'tags_year.txt']


def gen_statistic(pd_frame):
    res = []
    res.append(pd_frame.max(axis=0))
    res.append(pd_frame.min(axis=0))
    res.append(pd_frame.mean(axis=0))
    res.append(pd_frame.std(axis=0))
    res.append(pd_frame.var(axis=0))
    res.append(pd_frame.skew(axis=0))
    res.append(pd_frame.kurt(axis=0))
    res.append(pd_frame.median(axis=0))
    return res

def gen_feature(file_path):
    res = []
    df = pd.read_csv(file_path)
    nums = df["nums"]
    res.extend(gen_statistic(nums))
    incre = df["increment"].iloc[:-1]
    res.extend(gen_statistic(incre))
    ratio = df["ratio"].iloc[:-1]
    res.extend(gen_statistic(ratio))
    return res

def gen_head():
    colums = ["nums", "incre", "ratio"]
    stat = ['max', 'min', 'mean', 'std', 'var', 'skew', 'kurt', 'median']
    res = ''
    for f in file_names:
        part = f[:-4]
        for c in colums:
            for s in stat:
                res += ','
                tmp = part + '_' + c + '_' + s
                res += tmp
    return res + '\n'

def gen_dataset(data_path):
    all_data = os.listdir(data_path)
    all_feature = []
    with open('/Users/JDN/PycharmProjects/gitdata/software_rate.txt') as software:
        softwarelist = software.readlines()
    for software in softwarelist:
        software = software[:-1]
        feature = [software]
        path = data_path + '/' + software + '/'
        for fn in file_names:
            file_path = path + fn
            feature_part = gen_feature(file_path=file_path)
            feature.extend(feature_part)
        all_feature.append(feature)
    with open('/Users/JDN/PycharmProjects/gitdata/dataprocessing/feature.csv', 'w') as file:
        file.write(gen_head())
        for f in all_feature:
            line = ','.join([str(item) for item in f])
            line += '\n'
            file.write(line)


gen_dataset('/Users/JDN/stat')