# coding=utf-8
from __future__ import division
import pandas as pd
import numpy as np
import math
import datetime
import json
import os


# 本方法用于计算代码量级，即代码量取10的对数
# path为代码文件存储路径，software为软件名[owner_repo]
def Code_Volume(path, software, date):
    if os.path.exists(path + '/' + software + '_codes.xlsx'):
        xls_file = pd.ExcelFile(path + '/' + software + '_codes.xlsx').parse(0)
        if np.where(xls_file[u'时间'] == date)[0].size != 0:
            index = int(np.where(xls_file[u'时间'] == date)[0])
        else:
            print "Can't find " + date + ' code records!'
            return 0
        code = xls_file.iat[index, 1]
        codevolume = math.log(code, 10)
    else:
        codevolume = 0
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
    if len(list) != 0:
        mean = int(sum.days) / len(list)
    else:
        mean = None
    return mean


# 返回issues特征：
# 关闭问题数量，开放问题数量，已关闭问题平均持续时间，开放问题平均持续时间，开放问题占比
def issues_feature(path):  # path为issues.txt存储地址
    closed_duration, open_duration = issues_duration_list(path)
    closed_NUMS = len(closed_duration)
    open_NUMS = len(open_duration)
    if (open_NUMS + closed_NUMS) != 0:
        openratio = open_NUMS / (open_NUMS + closed_NUMS)
    else:
        openratio = None
    closed_duration_MEAN = duration_mean(closed_duration)
    open_duration_MEAN = duration_mean(open_duration)
    issues_feature_list = [closed_NUMS, open_NUMS, closed_duration_MEAN, open_duration_MEAN, openratio]
    return issues_feature_list


# 返回pulls特征：
# 关闭请求数量，合并请求数量，开放请求数量，
# 已关闭请求平均持续时间，已合并请求平均持续时间，开放请求平均持续时间，
# 开放请求占比，合并请求占比,拉取请求系数
def pulls_feature(path, codevolume):  # path为pulls.txt存储地址，codevolume为代码量级
    closed_duration, merged_duration, open_duration = pulls_duration_list(path)
    closed_NUMS = len(closed_duration)
    merged_NUMS = len(merged_duration)
    open_NUMS = len(open_duration)
    if (open_NUMS + closed_NUMS + merged_NUMS) != 0:
        openratio = open_NUMS / (open_NUMS + closed_NUMS + merged_NUMS)
        mergedratio = merged_NUMS / (open_NUMS + closed_NUMS + merged_NUMS)
    else:
        openratio = mergedratio = None

    closed_duration_MEAN = duration_mean(closed_duration)
    open_duration_MEAN = duration_mean(open_duration)
    merged_duration_MEAN = duration_mean(merged_duration)
    if codevolume != 0:
        pulls_FACTOR = (open_NUMS + closed_NUMS + merged_NUMS) / codevolume
    else:
        pulls_FACTOR = None
    pulls_feature_list = [closed_NUMS, merged_NUMS, open_NUMS,
                          closed_duration_MEAN, merged_duration_MEAN, open_duration_MEAN,
                          openratio, mergedratio, pulls_FACTOR]
    return pulls_feature_list


# 返回标签数、标签系数
def tags_feature(path, codevolume):
    with open(path + '/' + 'tags.txt') as f:
        tags = f.readlines()
        tags_NUMS = len(tags)
        if codevolume != 0:
            tags_FACTOR = tags_NUMS / codevolume
        else:
            tags_FACTOR = None
    tags_feature_list = [tags_NUMS, tags_FACTOR]
    return tags_feature_list


# 返回分支数、分支系数
def branches_feature(path, codevolume):
    with open(path + '/' + 'branches.txt') as f:
        branches = f.readlines()
        branches_NUMS = len(branches)
        if codevolume != 0:
            branches_FACTOR = branches_NUMS / codevolume
        else:
            branches_FACTOR = None
    branches_feature_list = [branches_NUMS, branches_FACTOR]
    return branches_feature_list


# 返回评论数、评论系数
def comments_feature(path, codevolume):
    with open(path + '/' + 'comments.txt') as f:
        comments = f.readlines()
        comments_NUMS = len(comments)
        if codevolume != 0:
            comments_FACTOR = comments_NUMS / codevolume
        else:
            comments_FACTOR = None
    comments_feature_list = [comments_NUMS, comments_FACTOR]
    return comments_feature_list


# 返回健康度
def communityhealth_feature(path):
    with open(path + '/' + 'community_profile.txt') as f:
        lines = f.readlines()
        health_percentage = json.loads(lines[0])['health_percentage']
    return health_percentage


# 返回提交数和贡献者的特征
def commits_contributors_feature(path, codevolume):
    commits_NUMS = 0
    contributors_NUMS = 0
    active_contributors_NUMS = 0
    contributors = {}
    active_contributors = {}  # ！列表里的值尚未利用！！
    with open(path + '/' + 'commits.txt') as f:
        for line in f.readlines():
            commits_NUMS += 1
            item = json.loads(line)
            # 统计贡献者总数，每个贡献者的提交数
            if not contributors.has_key(item["user_url"]):
                contributors[item["user_url"]] = 1
                contributors_NUMS += 1
            else:
                contributors[item["user_url"]] += 1
            # 统计活跃贡献者
            if item["date"][0:4] == '2018':
                if not active_contributors.has_key(item["user_url"]):
                    active_contributors[item["user_url"]] = 1
                    active_contributors_NUMS += 1
                else:
                    active_contributors[item["user_url"]] += 1
    active_ratio = active_contributors_NUMS / contributors_NUMS
    commits_person_avg = commits_NUMS / contributors_NUMS
    if codevolume != 0:
        commits_FACTOR = commits_NUMS / codevolume
        contributors_FACTOR = contributors_NUMS / codevolume
    else:
        commits_FACTOR = None
        contributors_FACTOR = None
    commits_contributors_feature_list = [commits_NUMS, commits_FACTOR, contributors_NUMS, contributors_FACTOR,
                                         commits_person_avg, active_contributors_NUMS, active_ratio]
    return commits_contributors_feature_list#, contributors, active_contributors


gitdatapath = '/Users/JDN/PycharmProjects/gitdata/gitdata'
codepath = '/Users/JDN/Desktop/1525745906613'

feature = []
with open('/Users/JDN/PycharmProjects/gitdata/software_rate.txt') as software:
    softwarelist = software.readlines()

for software in softwarelist:
    software = software[:-1]
    software_feature = [software]
    path = gitdatapath + '/' + software
    codevolume = Code_Volume(codepath, software, '2017-01-01')
    software_feature.append(codevolume)
    software_feature.extend(pulls_feature(path, codevolume))
    software_feature.extend(issues_feature(path))
    software_feature.extend(tags_feature(path, codevolume))
    software_feature.extend(comments_feature(path, codevolume))
    software_feature.extend(branches_feature(path, codevolume))
    software_feature.append(communityhealth_feature(path))
    software_feature.extend(commits_contributors_feature(path, codevolume))
    feature.append(software_feature)
    print software_feature

pulls_header = ['pull_closed_NUMS', 'pull_merged_NUMS', 'pull_open_NUMS',
                'pull_closed_duration_MEAN', 'pull_merged_duration_MEAN', 'pull_open_duration_MEAN',
                'pull_openratio', 'pull_mergedratio', 'pulls_FACTOR']
issues_header = ['issues_closed_NUMS', 'issues_open_NUMS', 'issues_closed_duration_MEAN', 'issues_open_duration_MEAN', 'issues_openratio']
tags_header = ['tags_NUMS', 'tags_FACTOR']
comments_header = ['comments_NUMS', 'comments_FACTOR']
branches_header = ['branches_NUMS', 'branches_FACTOR']
communityhealth_header = ['communityhealth']
commits_contributors_header = ['commits_NUMS', 'commits_FACTOR', 'contributors_NUMS', 'contributors_FACTOR',
                               'commits_person_avg', 'active_contributors_NUMS', 'active_ratio']

header = ['software','codevolume'] + pulls_header + issues_header + tags_header + comments_header + branches_header + communityhealth_header + commits_contributors_header
header = ','.join(header)
header += '\n'
with open('/Users/JDN/PycharmProjects/gitdata/dataprocessing/feature2.csv', 'w') as file:
    file.write(header)
    for f in feature:
        line = ','.join([str(item) for item in f])
        line += '\n'
        file.write(line)
