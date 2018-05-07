# coding=utf-8
import datetime
import json


# path为issues.txt存储地址
# 分别统计已关闭问题和开放问题的处理时长和问题个数
def issues_duration(path):
    closed_duration = []
    open_duration = []
    closed_num = 0
    open_num = 0
    with open(path) as f:
        for line in f.readlines():
            if json.loads(line)['state'] == 'closed':
                closed_num += 1
                created_at = datetime.datetime.strptime(json.loads(line)['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                closed_at = datetime.datetime.strptime(json.loads(line)['closed_at'], '%Y-%m-%dT%H:%M:%SZ')
                closed_duration.append(closed_at - created_at)
            else:
                open_num += 1
                created_at = datetime.datetime.strptime(json.loads(line)['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                today = datetime.datetime.today()
                open_duration.append(today - created_at)

    return closed_duration, closed_num,open_duration,open_num


# path为issues.txt存储地址
#分别统计已关闭、已合并、开放状态的pull request的处理时长和问题个数
def pulls_duration(path):
    closed_duration = []
    open_duration = []
    merged_duration =[]
    closed_num = 0
    merged_num = 0
    open_num = 0
    with open(path) as f:
        for line in f.readlines():
            if json.loads(line)['state'] == 'closed':
                if json.loads(line)['merged_at'] != None:
                    merged_num += 1
                    created_at = datetime.datetime.strptime(json.loads(line)['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                    merged_at = datetime.datetime.strptime(json.loads(line)['merged_at'], '%Y-%m-%dT%H:%M:%SZ')
                    merged_duration.append(merged_at - created_at)
                else:
                    closed_num += 1
                    created_at = datetime.datetime.strptime(json.loads(line)['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                    closed_at = datetime.datetime.strptime(json.loads(line)['closed_at'], '%Y-%m-%dT%H:%M:%SZ')
                    closed_duration.append(closed_at - created_at)
            else:
                open_num += 1
                created_at = datetime.datetime.strptime(json.loads(line)['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                today = datetime.datetime.today()
                open_duration.append(today - created_at)
    return closed_duration, closed_num, merged_duration,merged_num,open_duration,open_num
