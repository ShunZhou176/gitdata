# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 19:07:39 2018

@author: jiangdanni
"""

import json
import requests
import time
import os


def forks_get(repo_name, token):
    headers = {'Authorization': 'token ' + token}
    n = 1
    url = 'https://api.github.com/repos/'+repo_name+'/forks?page='+str(n)+'&per_page=100'
    resp = requests.get(url,headers=headers)
    fork =[]
    while(resp.status_code==200 and resp.json()!=[]):#翻页爬取内容直到为空
        data = resp.json()
        fork.append(data)
        time.sleep(0.5)
        n = n+1
        url = 'https://api.github.com/repos/'+repo_name+'/forks?page='+str(n)+'&per_page=100'
        resp = requests.get(url,headers=headers)
        print resp.status_code
        if resp.status_code == 403:
            print 'surpass time limit!'
            break
        if n % 10 == 0:
            print repo_name + ' get ' + str(n) + ' pages.'
    repo = repo_name.replace('/', '_')
    if not os.path.exists('data/' + repo):
        os.mkdir('data/' + repo)
    with open('data/' + repo + '/' + 'forks.json', 'w') as f:
        for items in fork:
            for item in items:
                todo = json.dumps(item['created_at'])
                f.write(todo + '\n')
def get_all_repo_forks(repo_name_path, token):
    if not os.path.exists('data'):
        os.mkdir('data')
    with open(repo_name_path, 'r') as f:
        for line in f:
            line = line.replace('\n', '')
            forks_get(line, token)
            print line + ' Finish.'



get_all_repo_forks('software.txt', 'b17ae20c8a2811cd336e0590ea5a3a11a31990e0')