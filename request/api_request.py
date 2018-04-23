#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# @Filename : api_request
# @Date : 2018-04-21-17-28
# @AUTHOR : bai
from threading import Thread
import requests
import time
import os
import json
import logging

class ApiRequst(object):
    def __init__(self, repo, apis):
        self.git_api_path_ = "https://api.github.com/repos"
        self.repo_ = repo
        self.repo_saved_ = repo.replace('/', '_')
        self.auth_limit_ = 5000
        self.common_limit_ = 100
        self.is_auth_ = False
        self.apis_ = []
        self.failed_codes_ = {}
        self.attrs_ = {}
        self.finished_ = {}
        self.logger_ = logging.getLogger(__name__)
        for api in apis:
            self.apis_.append(api[0])
            self.attrs_[api[0]] = api[1]
            self.finished_[api[0]] = False

    def get_url(self, api, page, page_size):
        url = self.git_api_path_ + '/' + self.repo_ + '/' +  api + '?page=' + str(page) + '&per_page=' + str(page_size)
        return url

    def get_header(self, token, api):
        if api == 'community/profile':
            header =  {'Accept': 'application/vnd.github.black-panther-preview+json', 'Authorization': 'token ' + token}
        else:
            header = {'Accept': 'application/vnd.github.v3.star+json', 'Authorization': 'token ' + token}
        return header

    def is_resp_fail(self, resp, api):
        if resp.status_code != 200 and resp.status_code != 422:
            self.logger_.info("Failed with status code " + str(resp.status_code))
            return True
        else:
            return False

    def is_end(self, resp):
        if resp.status_code == 422 or (resp.status_code == 200 and resp.json() == []):
            self.logger_.info("End with status code " + str(resp.status_code))
            return True
        else:
            return False

    def run_api(self, api, page, header):
        url = self.get_url(api, page, 100)
        resp = requests.get(url, headers=header)
        return resp

    def save_res(self, res, api):
        if not os.path.exists('gitdata'):
            os.mkdir('gitdata')
        if not os.path.exists('gitdata/' + self.repo_saved_):
            os.mkdir('gitdata/' + self.repo_saved_)
        file_name = 'gitdata/' + self.repo_saved_ + '/' + api.replace('/', '_') + '.txt'
        with open(file_name, 'w') as f:
            attr = self.attrs_[api]
            if len(attr) != 0:
                for item in res:
                    todo = json.dumps(item[attr])
                    f.write(todo + '\n')
            else:
                for item in res:
                    todo = json.dumps(item)
                    f.write(todo + '\n')

    def run_api_helper(self, api, token):
        file_name = 'gitdata/' + self.repo_saved_ + '/' + api.replace('/', '_') + '.txt'
        if os.path.exists(file_name):
            self.logger_.info(self.repo_saved_ + '/' + api + ' already in.')
            return
        if len(token) != 0:
            speed_limit = self.auth_limit_ / (60.0 * 60.0)
        else:
            speed_limit = self.common_limit_ / (60.0 * 60.0)
        call_count = 0
        start_time = time.time()
        is_failed = False
        res = []
        page = 1
        header = self.get_header(token, api)
        while True:
            resp = self.run_api(api, page, header)
            if self.is_end(resp):
                break
            # Retry server time
            if self.is_resp_fail(resp, api):
                retry_time = 5
                while self.is_resp_fail(resp, api) and retry_time > 0:
                    time.sleep(5)
                    retry_time -= 1
                    self.logger_.warning("retry: " + str(5 - retry_time))
                    resp = self.run_api(api, page, header)
                if self.is_resp_fail(resp, api):
                    is_failed = True
                    break
            res.extend(resp.json())
            new_time = time.time()
            call_count += 1
            speed = call_count / (new_time - start_time)
            if speed > speed_limit:
                wait_time = call_count / speed_limit - (new_time - start_time)
                self.logger_.warning("too quick, wait: " + str(wait_time))
                time.sleep(wait_time)
            page += 1
            if call_count % 20 == 0:
                self.logger_.info(self.repo_ + '/' + api + ':' + str(call_count))
        if not is_failed:
            self.save_res(res, api)
            self.finished_[api] = True
        self.logger_.info(self.repo_ + '/' + api + ' finished.')
        return

    def RunApi(self, api, token_pool):
        token = token_pool.Get()
        self.run_api_helper(api, token)
        token_pool.Return(token)

    def RunAll(self, token_pool):
        if not self.apis_:
            return
        threads = []
        for api in self.apis_:
            t = Thread(target=self.RunApi, args=(api, token_pool))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        self.logger_.info(self.repo_ + " all runned, ")
        if not os.path.exists('gitdata'):
            os.mkdir('gitdata')
        if not os.path.exists('gitdata/' + self.repo_saved_):
            os.mkdir('gitdata/' + self.repo_saved_)
            with open('gitdata/' + self.repo_saved_ + '/' + 'status.txt', 'w') as f:
                message = ''
                for key in self.finished_:

                    if self.finished_[key]:
                        message += key + ' finished\n'
                        f.write(key + ' finished\n')
                    else:
                        message += key + ' failed\n'
                        f.write(key + ' failed\n')
                self.logger_.info(message)