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
from worker_pool import global_worker_pool


class ApiRequest(object):
    def __init__(self, repo, apis):
        self.git_api_path_ = "https://api.github.com/repos"
        self.repo_ = repo
        self.repo_saved_ = repo.replace('/', '_')
        self.is_auth_ = False
        self.apis_ = []
        self.failed_codes_ = {}
        self.attrs_ = {}
        self.finished_ = {}
        self.logger_ = logging.getLogger(__name__)
        self.api_runner_ = {}
        self.api_extract_function_ = {
            "forks": self.get_forks,
            "subscribers": self.get_subscribers,
            "stargazers": self.get_stargazers,
            "commits": self.get_commits,
            "pulls": self.get_pulls,
            "issues": self.get_issues,
            "community/profile": self.get_profile,
            "tags": self.get_tags,
            "branches": self.get_branches,
            "comments": self.get_comments,
        }
        self.api_url_function_ ={
            "pulls": self.pulls_url,
            "issues": self.issues_url,
        }
        for api in apis:
            self.apis_.append(api[0])
            self.attrs_[api[0]] = api[1]
            self.finished_[api[0]] = False


    # -------------------------------------------------
    # Api url function begin.
    def pulls_url(self):
        '''
        https://developer.github.com/v3/pulls/#list-pull-requests
        '''
        return '&state=all'


    def issues_url(self):
        '''
        https://developer.github.com/v3/issues/#list-issues-for-a-repository
        '''
        return '&state=all'
    # Api url function end.
    # -------------------------------------------------


    # -------------------------------------------------
    # Api result extractor function begin.

    def get_forks(self, items, **kwargs):
        def get_fork_(item):
            return {"created_at" : item["created_at"],
                    "updated_at": item["updated_at"],
                    "pushed_at": item["pushed_at"]}
        return [get_fork_(item) for item in items]

    def get_subscribers(self, items, **kwargs):
        def get_subscriber_(item):
            return {"id": item["id"]}
        return [get_subscriber_(item) for item in items]

    def get_stargazers(self, items, **kwargs):
        def get_stargazer_(item):
            return {"starred_at": item["starred_at"]}
        return [get_stargazer_(item) for item in items]

    def get_commits(self, items, **kwargs):
        def get_commit_(item, worker):
            res = {
                   "date":"",
                   "user_url":""
                   }
            if item["commit"] != None and item["commit"]["author"] != None:
                res.update({"date": item["commit"]["author"]["date"]})
            if item["author"] != None and "url" in item["author"]:
                author_url = item["author"]["url"]
                res["user_url"] = author_url
            return res
        return [get_commit_(item, kwargs["worker"]) for item in items]

    def get_pulls(self, items, **kwargs):
        def get_pulls_(item):
            res = {"state": item["state"],
                   "created_at": item["created_at"],
                   "closed_at": item["closed_at"],
                   "merged_at": item["merged_at"]}
            return res
        return [get_pulls_(item) for item in items]

    def get_issues(self, items, **kwargs):
        def get_issue_(item):
            res = {"state": item["state"],
                   "created_at": item["created_at"],
                   "updated_at": item["updated_at"],
                   "closed_at": item["closed_at"]}
            return res
        return [get_issue_(item) for item in items]

    def get_profile(self, items, **kwargs):
        def get_profile_(item):
            res = {"health_percentage": item["health_percentage"],
                   "files": item["files"]}
            return res
        return [get_profile_(item) for item in items]

    def get_tags(self, items, **kwargs):
        def get_tag_(item, worker):
            commit_url = item["commit"]['url']
            header = self.get_header('commits')
            is_failed, resp = worker.run_api(commit_url, header)
            if not is_failed:
                res = {
                    "name": item["name"],
                    "date": resp.json()['commit']['committer']['date']
                }
            else:
                res = {
                    "name": item["name"],
                    "date": ''
                }
            return res
        return [get_tag_(item, kwargs['worker']) for item in items]

    def get_branches(self, items, **kwargs):
        res = items
        return res

    def get_comments(self, items, **kwargs):
        def get_comment_(item):
            res = {"created_at": item["created_at"],
                   "updated_at": item["updated_at"]}
            return res
        return [get_comment_(item) for item in items]

    # Api result extractor function end.
    # -------------------------------------------------

    def get_url(self, api, page, page_size):
        base_url = self.git_api_path_ + '/' + self.repo_ + '/' +  api + '?page=' + str(page) + '&per_page=' + str(page_size)
        append_resource = ''
        if api in self.api_url_function_:
            append_resource = self.api_url_function_[api]()
        return base_url + append_resource

    def get_header(self, api):
        if api == 'community/profile':
            header =  {'Accept': 'application/vnd.github.black-panther-preview+json', 'Authorization': 'token ' + '{0}'}
        else:
            header = {'Accept': 'application/vnd.github.v3.star+json', 'Authorization': 'token ' + '{0}'}
        return header


    def is_end(self, resp):
        if resp.status_code == 422 or (resp.status_code == 200 and resp.json() == []):
            self.logger_.info("End with status code " + str(resp.status_code))
            return True
        else:
            return False

    def save_res(self, res, api, worker):
        if not os.path.exists('gitdata'):
            os.mkdir('gitdata')
        if not os.path.exists('gitdata/' + self.repo_saved_):
            os.mkdir('gitdata/' + self.repo_saved_)
        file_name = 'gitdata/' + self.repo_saved_ + '/' + api.replace('/', '_') + '.txt'
        if api == 'commits':
            user_info = {}
            for item in res:
                if item["user_url"] != "":
                    user_info[item["user_url"]] = ""
            self.logger_.info(len(user_info))
            for url in user_info:
                header = self.get_header('users')
                is_failed, resp = worker.run_api(url, header)
                if not is_failed:
                    info = {
                        "company": resp.json()["company"],
                        "public_repos": resp.json()["public_repos"],
                        "public_gists": resp.json()["public_gists"],
                        "followers": resp.json()["followers"],
                        "user_created_at": resp.json()["created_at"]
                    }
                else:
                    info = {
                        "company": '',
                        "public_repos": '',
                        "public_gists": '',
                        "followers": '',
                        "user_created_at": ''
                    }
                user_info[url] = info
            for i in range(len(res)):
                if res[i]["user_url"] in user_info:
                    res[i].update(user_info[res[i]["user_url"]])
        with open(file_name, 'w') as f:
            for item in res:
                todo = json.dumps(item)
                f.write(todo + '\n')

    def run_api_helper(self, api):
        file_name = 'gitdata/' + self.repo_saved_ + '/' + api.replace('/', '_') + '.txt'
        if os.path.exists(file_name):
            self.logger_.info(self.repo_saved_ + '/' + api + ' already in.')
            return
        res = []
        page = 1
        header = self.get_header(api)
        worker = global_worker_pool.get_worker()
        while True:
            url = self.get_url(api, page, 100)
            is_failed, resp = worker.run_api(url, header)
            if is_failed or self.is_end(resp):
                break
            fuc = self.api_extract_function_[api]
            if not isinstance(resp.json(), list):
                res_list = [resp.json()]
            else:
                res_list = resp.json()
            res.extend(fuc(res_list, worker=worker))
            page += 1
            if page % 1 == 0:
                self.logger_.info(self.repo_ + '/' + api + ' page :' + str(page))
            if api == 'community/profile':
                break

        if not is_failed:
            self.save_res(res, api, worker=worker)
            self.finished_[api] = True
        global_worker_pool.return_worker(worker)
        self.logger_.info(self.repo_ + '/' + api + ' finished.')
        return

    def RunAll(self):
        if not self.apis_:
            return
        threads = []
        for api in self.apis_:
            if api in self.api_runner_:
                t = Thread(target=self.api_runner_[api])
            else:
                t = Thread(target=self.run_api_helper, args=[api])
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