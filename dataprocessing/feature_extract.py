# coding=utf-8
from __future__ import division
import pandas as pd
import numpy as np
import math
import datetime
import json


# 本方法用于计算代码量级，即代码量取10的对数
# path为代码文件存储路径，software为软件名[owner_repo]
def Code_Volume(path, software, date):
    xls_file = pd.ExcelFile(path + '/' + software + '_codes.xlsx').parse(0)
    if np.where(xls_file == date)[0].size != 0:
        index = int(np.where(xls_file == date)[0])
    else:
        print "Can't find " + date + ' code records!'
        return 0
    code = xls_file.iat[index, 1]
    codevolume = math.log(code, 10)
    return codevolume


# 本方法返回订阅数，分叉数，加星数，社区影响力系数=(watch+fork+star)/代码量级
# path为存放subscribers，forks，stargazers文件的路径
def CommunityImpact(path, codevolume):
    with open(path + '/' + 'subscribers.txt')as f:
        lines = f.readlines()
        subscribers = len(lines)
    with open(path + '/' + 'forks.txt')as f:
        lines = f.readlines()
        forks = len(lines)
    with open(path + '/' + 'stargazers.txt')as f:
        lines = f.readlines()
        stargazers = len(lines)
    communityimpact = (subscribers + forks + stargazers) / codevolume
    return subscribers, forks, stargazers, communityimpact


# 本方法返回已关闭问题和开放问题的处理时长,返回list
# path为issues.txt存储地址
def issues_duration_list(path):
    closed_duration = []
    open_duration = []
    with open(path + '/' + 'issues.txt') as f:
        for line in f.readlines():
            if json.loads(line)['state'] == 'closed':
                created_at = datetime.datetime.strptime(json.loads(line)['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                closed_at = datetime.datetime.strptime(json.loads(line)['closed_at'], '%Y-%m-%dT%H:%M:%SZ')
                closed_duration.append(closed_at - created_at)
            else:
                created_at = datetime.datetime.strptime(json.loads(line)['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                today = datetime.datetime.today()
                open_duration.append(today - created_at)

    return closed_duration, open_duration


# 本方法返回已关闭、已合并、开放状态的pull request的处理时长,返回list
# path为pulls.txt存储地址
def pulls_duration_list(path):
    closed_duration = []
    open_duration = []
    merged_duration = []
    with open(path + '/' + 'pulls.txt') as f:
        for line in f.readlines():
            if json.loads(line)['state'] == 'closed':
                if json.loads(line)['merged_at'] != None:
                    created_at = datetime.datetime.strptime(json.loads(line)['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                    merged_at = datetime.datetime.strptime(json.loads(line)['merged_at'], '%Y-%m-%dT%H:%M:%SZ')
                    merged_duration.append(merged_at - created_at)
                else:
                    created_at = datetime.datetime.strptime(json.loads(line)['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                    closed_at = datetime.datetime.strptime(json.loads(line)['closed_at'], '%Y-%m-%dT%H:%M:%SZ')
                    closed_duration.append(closed_at - created_at)
            else:
                created_at = datetime.datetime.strptime(json.loads(line)['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                today = datetime.datetime.today()
                open_duration.append(today - created_at)
    return closed_duration, merged_duration, open_duration


# 返回平均时长（天数）
# list存储datetime.timedelta()类型
def duration_mean(list):
    sum = datetime.timedelta(0)
    for item in list:
        sum += item
    mean = int(sum.days) / len(list)
    return mean


# 返回issues特征：
# 关闭问题数量，开放问题数量，已关闭问题平均持续时间，开放问题平均持续时间，开放问题占比
def issues_feature(path):  # path为issues.txt存储地址
    closed_duration, open_duration = issues_duration_list(path)
    closed_NUMS = len(closed_duration)
    open_NUMS = len(open_duration)
    openratio = open_NUMS / (open_NUMS + closed_NUMS)
    closed_duration_MEAN = duration_mean(closed_duration)
    open_duration_MEAN = duration_mean(open_duration)
    return closed_NUMS, open_NUMS, closed_duration_MEAN, open_duration_MEAN, openratio


# 返回pulls特征：
# 关闭请求数量，合并请求数量，开放请求数量，
# 已关闭请求平均持续时间，已合并请求平均持续时间，开放请求平均持续时间，
# 开放请求占比，合并请求占比,拉取请求系数
def pulls_feature(path, codevolume):  # path为pulls.txt存储地址，codevolume为代码量级
    closed_duration, merged_duration, open_duration = pulls_duration_list(path)
    closed_NUMS = len(closed_duration)
    merged_NUMS = len(merged_duration)
    open_NUMS = len(open_duration)
    openratio = open_NUMS / (open_NUMS + closed_NUMS + merged_NUMS)
    mergedratio = merged_NUMS / (open_NUMS + closed_NUMS + merged_NUMS)
    closed_duration_MEAN = duration_mean(closed_duration)
    open_duration_MEAN = duration_mean(open_duration)
    merged_duration_MEAN = duration_mean(merged_duration)
    if codevolume != 0:
        pulls_FACTOR = (open_NUMS + closed_NUMS + merged_NUMS) / codevolume
    else:
        pulls_FACTOR = None
    return closed_NUMS, merged_NUMS, open_NUMS, closed_duration_MEAN, merged_duration_MEAN, open_duration_MEAN, openratio, mergedratio, pulls_FACTOR


# 返回标签数、标签系数
def tags_feature(path, codevolume):
    with open(path + '/' + 'tags.txt') as f:
        tags = f.readlines()
        tags_NUMS = len(tags)
        if codevolume != 0:
            tags_FACTOR = tags_NUMS / codevolume
        else:
            tags_FACTOR = None
    return tags_NUMS, tags_FACTOR


# 返回分支数、分支系数
def branches_feature(path, codevolume):
    with open(path + '/' + 'branches.txt') as f:
        branches = f.readlines()
        branches_NUMS = len(branches)
        if codevolume != 0:
            branches_FACTOR = branches_NUMS / codevolume
        else:
            branches_FACTOR = None
    return branches_NUMS, branches_FACTOR


# 返回评论数、评论系数
def comments_feature(path, codevolume):
    with open(path + '/' + 'comments.txt') as f:
        comments = f.readlines()
        comments_NUMS = len(comments)
        if codevolume != 0:
            comments_FACTOR = comments_NUMS / codevolume
        else:
            comments_FACTOR = None
    return comments_NUMS, comments_FACTOR


# 返回健康度
def communityhealth_feature(path):
    with open(path + '/' + 'community_profile.txt') as f:
        lines = f.readlines()
        health_percentage = json.loads(lines[0])['health_percentage']
    return health_percentage


gitdatapath = 'D:/githubdata/alibaba_fastjson'
codepath = 'C:/Users/jiangdanni/Desktop/1525745906613'

feature = []
codevolume = Code_Volume(codepath, 'alibaba_fastjson', '2018-01-01')
print 'codevolume:' + str(codevolume)
feature.extend(CommunityImpact(gitdatapath, codevolume))
feature.extend(pulls_feature(gitdatapath,codevolume))


