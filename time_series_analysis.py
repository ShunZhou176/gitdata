#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json


# 统计每月的出现频率
def get_nums_month(timestamp_list):  # timestamp_list为包含一组时间戳的列表，例如2018-04-16T15:40:32Z
    nums_month = {}
    for line in timestamp_list:
        month = line[0:7]
        if nums_month.has_key(month) == False:
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


with open('D:/gitdata/example_data/apache_activemq/forks.txt', 'r') as f:
    data = []
    for line in f.readlines():
        data.append(json.loads(line)['created_at'])
print data
