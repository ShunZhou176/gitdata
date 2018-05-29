# coding=utf-8
from __future__ import division

import os
import json
import pandas as pd
from datetime import datetime


# 统计每月的出现频率
def get_nums_month(timestamp_list):  # timestamp_list为包含一组时间戳的列表，例如2018-04-16T15:40:32Z
    datelist = []
    if timestamp_list != [] and timestamp_list is not None:
        nums_month = {}
        for line in timestamp_list:
            month = line[0:7]
            if not nums_month.has_key(month):
                nums_month[month] = 1
            else:
                nums_month[month] += 1
        timelist = sorted([[k, nums_month[k]] for k in nums_month], key=lambda x: x[0], reverse=True)
        date_l = [datetime.strftime(x, '%Y-%m') for x in
                  list(pd.date_range(start=timelist[-1][0], end=timelist[0][0], freq='M'))]
        for date in date_l:
            if nums_month.has_key(date):
                datelist.append([date, nums_month[date]])
            else:
                datelist.append([date, 0])
        datelist.append(timelist[0])
        datelist.reverse()
    return datelist


# 统计每月,每季度,每年的出现频率
def get_nums(timestamp_list):  # timestamp_list为包含一组时间戳的列表，例如2018-04-16T15:40:32Z

    # 月份
    monthlist = get_nums_month(timestamp_list)

    # 季度
    nums_quart = {}
    for line in monthlist:
        m = int(line[0][5:7])
        y = line[0][0:4]
        if m < 4:
            quart = y + '-Q1'
        elif m < 7:
            quart = y + '-Q2'
        elif m < 10:
            quart = y + '-Q3'
        else:
            quart = y + '-Q4'
        if nums_quart.has_key(quart) == False:
            nums_quart[quart] = line[1]
        else:
            nums_quart[quart] += line[1]
    quartlist = sorted([[k, nums_quart[k]] for k in nums_quart], key=lambda x: x[0], reverse=True)

    # 年份
    nums_year = {}
    for line in quartlist:
        year = line[0][0:4]
        if nums_year.has_key(year) == False:
            nums_year[year] = line[1]
        else:
            nums_year[year] += line[1]
    yearlist = sorted([[k, nums_year[k]] for k in nums_year], key=lambda x: x[0], reverse=True)
    return monthlist, quartlist, yearlist


# 同时计算环比增量和变化率,date_num_list格式为[date,num]
# 时间顺序为由近到远
def get_increment(date_num_list):
    data_list = []
    if date_num_list != [] and date_num_list is not None:
        for i in range(len(date_num_list) - 1):
            increment = date_num_list[i][1] - date_num_list[i + 1][1]
            if date_num_list[i + 1][1] != 0:
                ratio = increment / date_num_list[i + 1][1]
            else:
                ratio = 0
            data_list.append([date_num_list[i][0], date_num_list[i][1], increment, ratio])
        data_list.append([date_num_list[-1][0], date_num_list[-1][1], 0, 0])  # 最后一条数据增量和变化率为0
    return data_list


def read_json(attr, line):
    if attr == 'stargazers':
        return json.loads(line)['starred_at']
    if attr == 'forks':
        return json.loads(line)['created_at']
    if attr == 'comments':
        return json.loads(line)['created_at']
    if attr == 'commits':
        return json.loads(line)['date']
    if attr == 'issues':
        return json.loads(line)['created_at']
    if attr == 'pulls':
        return json.loads(line)['created_at']
    if attr == 'tags':
        return json.loads(line)['date']


def get_all_software_stat(path, outpath, attr):
    with open('/Users/JDN/PycharmProjects/gitdata/software_rate.txt') as software:
        softwarelist = software.readlines()
    if not os.path.exists(outpath):  # 输出文件夹若不存在则新建一个
        os.mkdir(outpath)
    for fdir in softwarelist:
        fdir = fdir[:-1]
        print fdir
        data = []
        if not os.path.exists(outpath + '/' + fdir):  # 输出文件夹若不存在则新建一个
            os.mkdir(outpath + '/' + fdir)
        if '.DS_Store' not in fdir:
            with open(path + '/' + fdir + '/' + attr + '.txt', 'r') as f:
                for line in f.readlines():
                    data.append(read_json(attr, line))  # 读取时间戳列表
            month_list, quart_list, year_list = get_nums(data)
            year_incre_list = get_increment(year_list)
            quart_incre_list = get_increment(quart_list)
            month_incre_list = get_increment(month_list)
            head = ['date', 'nums', 'increment', 'ratio']
            year_df = pd.DataFrame(year_incre_list, columns=head)
            quart_df = pd.DataFrame(quart_incre_list, columns=head)
            month_df = pd.DataFrame(month_incre_list, columns=head)
            year_df.to_csv(outpath + '/' + fdir + '/' + attr + '_year.csv')
            quart_df.to_csv(outpath + '/' + fdir + '/' + attr + '_quart.csv')
            month_df.to_csv(outpath + '/' + fdir + '/' + attr + '_month.csv')


def get_all_software_stat_recent(path, outpath, attr):
    with open('/Users/JDN/PycharmProjects/gitdata/software_rate.txt') as software:
        softwarelist = software.readlines()
    if not os.path.exists(outpath):  # 输出文件夹若不存在则新建一个
        os.mkdir(outpath)
    for fdir in softwarelist:
        fdir = fdir[:-1]
        print fdir
        data = []
        if not os.path.exists(outpath + '/' + fdir):  # 输出文件夹若不存在则新建一个
            os.mkdir(outpath + '/' + fdir)
        if '.DS_Store' not in fdir:
            with open(path + '/' + fdir + '/' + attr + '.txt', 'r') as f:
                for line in f.readlines():
                    data.append(read_json(attr, line))  # 读取时间戳列表

            #————————————截取最近两年数据——————————————————
            month, quart, year = get_nums(data)
            year_list = []
            quart_list = []
            month_list = []
            for data in month:
                if data[0][0:4] in {'2016','2017','2018'}:
                    month_list.append(data)
                else:
                    break
            for data in quart:
                if data[0][0:4] in {'2016','2017','2018'}:
                    quart_list.append(data)
                else:
                    break
            for data in year:
                if data[0][0:4] in {'2016','2017','2018'}:
                    year_list.append(data)
                else:
                    break
            #————————————截取最近两年数据——————————————————
            year_incre_list = get_increment(year_list)
            quart_incre_list = get_increment(quart_list)
            month_incre_list = get_increment(month_list)
            head = ['date', 'nums', 'increment', 'ratio']
            year_df = pd.DataFrame(year_incre_list, columns=head)
            quart_df = pd.DataFrame(quart_incre_list, columns=head)
            month_df = pd.DataFrame(month_incre_list, columns=head)
            year_df.to_csv(outpath + '/' + fdir + '/' + attr + '_year.csv')
            quart_df.to_csv(outpath + '/' + fdir + '/' + attr + '_quart.csv')
            month_df.to_csv(outpath + '/' + fdir + '/' + attr + '_month.csv')


attr_list = ['stargazers', 'forks', 'comments', 'commits', 'issues', 'pulls', 'tags']
# path = '/Users/JDN/data'  # path 读取数据文件路径
# outpath = '/Users/JDN/stat'  # outpath 输出文件路径
path = '/Users/JDN/PycharmProjects/gitdata/gitdata'
outpath = '/Users/JDN/stat'
for attr in attr_list:
    get_all_software_stat(path, outpath, attr)
