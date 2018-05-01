# coding=utf-8
from __future__ import division

import os
import json
import pandas as pd


# 统计每月的出现频率
def get_nums_month(timestamp_list):  # timestamp_list为包含一组时间戳的列表，例如2018-04-16T15:40:32Z
    nums_month = {}
    for line in timestamp_list:
        month = line[0:7]
        if not nums_month.has_key(month):
            nums_month[month] = 1
        else:
            nums_month[month] += 1
    return sorted([[k, nums_month[k]] for k in nums_month], key=lambda x: x[0], reverse=True)


# 统计每季度的出现频率
def get_nums_quart(timestamp_list):  # timestamp_list为包含一组时间戳的列表，例如2018-04-16T15:40:32Z
    nums_quart = {}
    for line in timestamp_list:
        m = int(line[5:7])
        y = line[0:4]
        if m < 4:
            quart = y + 'q1'
        elif m < 7:
            quart = y + 'q2'
        elif m < 10:
            quart = y + 'q3'
        else:
            quart = y + 'q4'
        if nums_quart.has_key(quart) == False:
            nums_quart[quart] = 1
        else:
            nums_quart[quart] += 1
    return sorted([[k, nums_quart[k]] for k in nums_quart], key=lambda x: x[0], reverse=True)


# 统计每年的出现频率
def get_nums_year(timestamp_list):  # timestamp_list为包含一组时间戳的列表，例如2018-04-16T15:40:32Z
    nums_year = {}
    for line in timestamp_list:
        year = line[0:4]
        if nums_year.has_key(year) == False:
            nums_year[year] = 1
        else:
            nums_year[year] += 1
    return sorted([[k, nums_year[k]] for k in nums_year], key=lambda x: x[0], reverse=True)


# 同时计算环比增量和变化率,date_num_list格式为[date,num]
# 时间顺序为由近到远
def get_increment(date_num_list):
    data_list = []
    if date_num_list != []:
        for i in range(len(date_num_list) - 1):
            increment = date_num_list[i][1] - date_num_list[i + 1][1]
            ratio = increment / date_num_list[i + 1][1]
            data_list.append([date_num_list[i][0], date_num_list[i][1], increment, ratio])
        data_list.append([date_num_list[-1][0], date_num_list[-1][1], 0, 0])  # 最后一条数据增量和变化率为0
    return data_list



def get_all_stargazers_stat(path, outpath):
    name = 'stargazers'
    fs = os.listdir(path)
    if not os.path.exists(outpath + '/' + name):  # 输出文件夹若不存在则新建一个
        os.mkdir(outpath + '/' + name)
    for fdir in fs:
        print fdir
        data = []
        if '.DS_Store' not in fdir:
            with open(path + '/' + fdir + '/' + name + '.txt', 'r') as f:
                for line in f.readlines():
                    data.append(json.loads(line)['starred_at'])  # 读取时间戳列表
            month_list = get_nums_month(data)
            increment_list = get_increment(month_list)
            head = ['date', 'nums', 'increment', 'ratio']
            df = pd.DataFrame(increment_list, columns=head)
            df.to_csv(outpath + '/' + name + '/' + fdir + '.txt')


def get_all_forks_stat(path, outpath):  # 遍历所有软件文件夹下的forks文件，计算统计量，输出到单独的文件夹下
    name = 'forks'
    fs = os.listdir(path)
    if not os.path.exists(outpath + '/' + name):  # 输出文件夹若不存在则新建一个
        os.mkdir(outpath + '/' + name)
    for fdir in fs:
        print fdir
        data = []
        if '.DS_Store' not in fdir:
            with open(path + '/' + fdir + '/' + name + '.txt', 'r') as f:
                for line in f.readlines():
                    data.append(json.loads(line)['created_at'])  # 读取时间戳列表
            month_list = get_nums_month(data)
            increment_list = get_increment(month_list)
            head = ['date', 'nums', 'increment', 'ratio']
            df = pd.DataFrame(increment_list, columns=head)
            df.to_csv(outpath + '/' + name + '/' + fdir + '.txt')


def get_all_comments_stat(path, outpath):
    name = 'comments'
    fs = os.listdir(path)
    if not os.path.exists(outpath + '/' + name):  # 输出文件夹若不存在则新建一个
        os.mkdir(outpath + '/' + name)
    for fdir in fs:
        print fdir
        data = []
        if '.DS_Store' not in fdir:
            with open(path + '/' + fdir + '/' + name + '.txt', 'r') as f:
                for line in f.readlines():
                    data.append(json.loads(line)['created_at'])  # 读取时间戳列表
            month_list = get_nums_month(data)
            increment_list = get_increment(month_list)
            head = ['date', 'nums', 'increment', 'ratio']
            df = pd.DataFrame(increment_list, columns=head)
            df.to_csv(outpath + '/' + name + '/' + fdir + '.txt')


def get_all_commits_stat(path, outpath):
    name = 'commits'
    fs = os.listdir(path)
    if not os.path.exists(outpath + '/' + name):  # 输出文件夹若不存在则新建一个
        os.mkdir(outpath + '/' + name)
    for fdir in fs:
        print fdir
        data = []
        if '.DS_Store' not in fdir:
            with open(path + '/' + fdir + '/' + name + '.txt', 'r') as f:
                for line in f.readlines():
                    data.append(json.loads(line)['committer']['date'])  # 读取时间戳列表
            month_list = get_nums_month(data)
            increment_list = get_increment(month_list)
            head = ['date', 'nums', 'increment', 'ratio']
            df = pd.DataFrame(increment_list, columns=head)
            df.to_csv(outpath + '/' + name + '/' + fdir + '.txt')

def get_all_issues_stat(path, outpath):
    name = 'issues'
    fs = os.listdir(path)
    if not os.path.exists(outpath + '/' + name):  # 输出文件夹若不存在则新建一个
        os.mkdir(outpath + '/' + name)
    for fdir in fs:
        print fdir
        data = []
        if '.DS_Store' not in fdir:
            with open(path + '/' + fdir + '/' + name + '.txt', 'r') as f:
                for line in f.readlines():
                    data.append(json.loads(line)['created_at'])  # 读取时间戳列表
            month_list = get_nums_month(data)
            increment_list = get_increment(month_list)
            head = ['date', 'nums', 'increment', 'ratio']
            df = pd.DataFrame(increment_list, columns=head)
            df.to_csv(outpath + '/' + name + '/' + fdir + '.txt')


def get_all_pulls_stat(path, outpath):
    name = 'pulls'
    fs = os.listdir(path)
    if not os.path.exists(outpath + '/' + name):  # 输出文件夹若不存在则新建一个
        os.mkdir(outpath + '/' + name)
    for fdir in fs:
        print fdir
        data = []
        if '.DS_Store' not in fdir:
            with open(path + '/' + fdir + '/' + name + '.txt', 'r') as f:
                for line in f.readlines():
                    data.append(json.loads(line)['created_at'])  # 读取时间戳列表
            month_list = get_nums_month(data)
            increment_list = get_increment(month_list)
            head = ['date', 'nums', 'increment', 'ratio']
            df = pd.DataFrame(increment_list, columns=head)
            df.to_csv(outpath + '/' + name + '/' + fdir + '.txt')


path = '/Users/JDN/data'  # path 读取数据文件路径
outpath = '/Users/JDN/stat'  # outpath 输出文件路径
get_all_pulls_stat(path,outpath)
