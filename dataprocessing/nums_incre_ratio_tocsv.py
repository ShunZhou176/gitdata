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


def read_json(attr,line):
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
                    data.append(read_json(attr,line))  # 读取时间戳列表
            month_list = get_nums_month(data)
            quart_list = get_nums_quart(data)
            year_list = get_nums_year(data)
            year_increment_list = get_increment(year_list)
            quart_increment_list = get_increment(quart_list)
            month_increment_list = get_increment(month_list)
            head = ['date', 'nums', 'increment', 'ratio']
            year_df = pd.DataFrame(year_increment_list, columns=head)
            quart_df = pd.DataFrame(quart_increment_list, columns=head)
            month_df = pd.DataFrame(month_increment_list, columns=head)
            year_df.to_csv(outpath + '/' + fdir + '/' + attr + '_year.txt')
            quart_df.to_csv(outpath + '/' + fdir + '/' + attr + '_quart.txt')
            month_df.to_csv(outpath + '/' + fdir + '/' + attr + '_month.txt')



attr_list = ['stargazers','forks','comments','commits','issues','pulls','tags']
#path = '/Users/JDN/data'  # path 读取数据文件路径
#outpath = '/Users/JDN/stat'  # outpath 输出文件路径
path = '/Users/JDN/PycharmProjects/gitdata/gitdata'
outpath = '/Users/JDN/stat'
for attr in attr_list:
    get_all_software_stat(path,outpath,attr)