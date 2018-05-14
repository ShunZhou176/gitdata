import Queue
import time
import requests
import logging
import json
import traceback
from utils import safe_while

class CrawlerRobot(object):
    def __init__(self, token, hour_limit):
        self.token_ = token
        self.speed_limit_ = hour_limit / (60.0 * 60.0)
        self.run_times_ = 0
        self.start_time_ = time.time()
        self.logger_ = logging.getLogger(__name__)

    def is_resp_fail(self, resp):
        if resp.status_code != 200 and resp.status_code != 422:
            self.logger_.info("Failed with status code " + str(resp.status_code))
            return True
        else:
            return False

    def get_header_(self, header_template):
        pass
    def run_api_(self, url, header_template):
        header_template['Authorization'] = header_template['Authorization'].format(self.token_)
        success = False
        with safe_while(
                sleep=6, increment=0.5, action=url, _raise=False) as proceed:
            while proceed():
                try:
                    resp = requests.get(url, headers=header_template)
                    return False, resp
                # Work around https://github.com/kennethreitz/requests/issues/2364
                except requests.exception.ConnectionError as e:
                    self.logger_.warn("Saw %s while unlocking; retrying...", str(e))
        return True, None
        # try:
        #     resp = requests.get(url, headers=header_template)
        # except Exception as e:
        #     self.logger_.error("type error: " + str(e))
        #     self.logger_.error(traceback.format_exc())
        #     return True, []
        # return False, resp

    def run_api(self, url, header):
        failed, resp = self.run_api_(url, header)
        if failed:
            return True, []
        is_failed = False
        if self.is_resp_fail(resp):
            retry_time = 5
            while self.is_resp_fail(resp) and retry_time > 0:
                time.sleep(5)
                retry_time -= 1
                self.logger_.warning("retry: " + str(5 - retry_time))
                resp = self.run_api_(url, header)
            if self.is_resp_fail(resp):
                is_failed = True
        if is_failed:
            return is_failed, resp
        new_time = time.time()
        self.run_times_ += 1
        speed = self.run_times_ / (new_time - self.start_time_)
        if speed > self.speed_limit_:
            wait_time = self.run_times_ / self.speed_limit_ - (new_time - self.start_time_)
            self.logger_.warning("too quick, wait: " + str(wait_time))
            time.sleep(wait_time)
        return is_failed, resp


class WorkerPool(object):
    def __init__(self):
        self.worker_queue_ = Queue.Queue()
        self.logger_ = logging.getLogger(__name__)

    def init(self, tokens):
        nn = len(tokens)
        if nn == 0:
            self.logger_.error("No worker available.")
            return False
        for i in range(nn):
            worker = CrawlerRobot(tokens[i], 5000)
            self.worker_queue_.put(worker)
        return True

    def return_worker(self, worker):
        self.worker_queue_.put(worker)

    def get_worker(self):
        return self.worker_queue_.get()


# token pool singleton
global_worker_pool = WorkerPool()
