# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 19:10:56 2018

@author: jiangdanni
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import json
import requests
import time
import os




def subscriber_get(repo_name, token):
    headers = {'Authorization': 'token ' + token}
    n = 1
    url = 'https://api.github.com/repos/'+repo_name+'/subscribers?page='+str(n)+'&per_page=100'
    resp = requests.get(url,headers=headers)
    subs =[]
    subs_num = 0
    
    while(resp.status_code==200 and resp.json()!=[]):#翻页爬取内容直到为空
        data = resp.json()
        subs.append(data)
        subs_num = subs_num+len(data)
        time.sleep(0.5)
        n = n+1
        url = 'https://api.github.com/repos/'+repo_name+'/subscribers?page='+str(n)+'&per_page=100'
        resp = requests.get(url,headers=headers)
        if resp.status_code == 403:
            print 'surpass time limit!'
            break
        if n % 10 == 0:
            print repo_name + ' get ' + str(n) + ' pages.'
    return subs_num
  
         
    
def get_all_repo_subscriber(repo_name_path,token):
    subscriber_set = []
    if not os.path.exists('data'):
        os.mkdir('data')
   
    with open(repo_name_path, 'r') as f:
        for line in f:
            line = line.replace('\n', '')
            num = subscriber_get(line, token)
            subscriber_set.append(line +','+ str(num))
    with open('data/' + 'forks.json', 'w') as f:
        for line in subscriber_set:
            f.write(line + '\n')
    print 'apache/kafka' + num



get_all_repo_subscriber('software.txt', '7f6f47c7724a0de31a094550d0d2c4792738b737')
    
    