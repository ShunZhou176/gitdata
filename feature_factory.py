import numpy as np
import pandas as pd
import os
file_names = [
 # 'commits_month.txt',
 # 'commits_year.txt',
 'forks_month.txt',
 'forks_year.txt',
 'issues_month.txt',
 'issues_year.txt',
 'pulls_month.txt',
 'pulls_year.txt',
 'stargazers_month.txt',
 'stargazers_year.txt']


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
    for software in all_data:
        feature = [software]
        path = data_path + '/' + software + '/'
        for fn in file_names:
            file_path = path + fn
            feature_part = gen_feature(file_path=file_path)
            feature.extend(feature_part)
        all_feature.append(feature)
    with open('feature.csv', 'w') as file:
        file.write(gen_head())
        for f in all_feature:
            line = ','.join([str(item) for item in f])
            line += '\n'
            file.write(line)


gen_dataset('D:/stat')