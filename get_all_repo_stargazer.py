# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import json
import requests
import time
import os




def stargazer_get(repo_name, token):
    headers = {'Accept':'application/vnd.github.v3.star+json','Authorization': 'token ' + token}
    n = 1
    url = 'https://api.github.com/repos/'+repo_name+'/stargazers?page='+str(n)+'&per_page=100'
    resp = requests.get(url,headers=headers)
    star =[]
    while(resp.status_code!=422 and resp.json()!=[]):#翻页爬取内容直到为空
        data = resp.json()
        star.append(data)
        time.sleep(1)
        n = n+1
        url = 'https://api.github.com/repos/'+repo_name+'/stargazers?page='+str(n)+'&per_page=100'
        resp = requests.get(url,headers=headers)
        if resp.status_code == 403:
            print 'surpass time limit!'
            break
        if n % 10 == 0:
            print repo_name + ' get ' + str(n) + ' pages.'
    repo = repo_name.replace('/', '_')
    if not os.path.exists('data/' + repo):
        os.mkdir('data/' + repo)
    with open('data/' + repo + '/' + 'stars.json', 'w') as f:
        for items in star:
            for item in items:
                todo = json.dumps(item['starred_at'])
                f.write(todo + '\n')
def get_all_repo_stargazer(repo_name_path, token):
    if not os.path.exists('data'):
        os.mkdir('data')
    with open(repo_name_path, 'r') as f:
        for line in f:
            line = line.replace('\n', '')
            stargazer_get(line, token)
            print line + ' Finish.'



get_all_repo_stargazer('software.txt', '1f36762834ebf5cb4b95cd3d74db4413d6b7ba7f')
    
    