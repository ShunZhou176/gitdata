#!/usr/bin/env python2
#-*- coding: utf-8 -*-
#@Filename : main
#@Date : 2018-04-21-22-18
#@AUTHOR : bai
from request.token_pool import global_token_pool
from request.api_request import ApiRequst
from threading import Thread
import argparse
import logging
import logging.config
import os
import json
def get_tokens(token_path):
    res = []
    with open(token_path, 'r') as f:
        for line in f:
            line = line.replace('\n', '')
            res.append(line)
    return res


def get_apis(api_path):
    res = []
    with open(api_path, 'r') as f:
        for line in f:
            line = line.replace('\n', '')
            res.append(line.split(','))
    return res


def get_softwares(software_path):
    res = []
    with open(software_path, 'r') as f:
        for line in f:
            line = line.replace('\n', '')
            res.append(line)
    return res
def setup_logging(
    default_path='logger.json',
    default_level=logging.INFO,
    env_key='LOG_CFG',
    log_directory='logs'
):
    """Setup logging configuration

    """
    if not os.path.exists(log_directory):
	os.mkdir(log_directory)
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)

    else:
        logging.basicConfig(level=default_level)

def main(token_path, api_path, software_path):
    setup_logging()
    logger = logging.getLogger(__name__)
    tokens = get_tokens(token_path)
    global_token_pool.Init(tokens)

    apis = get_apis(api_path)
    softwares = get_softwares(software_path)

    api_requests = []
    for s in softwares:
        req = ApiRequst(s, apis)
        api_requests.append(req)
    threads = []
    for api in api_requests:
        t = Thread(target=api.RunAll, args=[global_token_pool])
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    logger.info("All done.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--token_path", type=str, default="", help="all tokens")
    parser.add_argument("--api_path", type=str, default="", help="all apis")
    parser.add_argument("--software_path", type=str, default="", help="software path")
    FLAGS, unparsered = parser.parse_known_args()
    main(FLAGS.token_path, FLAGS.api_path, FLAGS.software_path)
