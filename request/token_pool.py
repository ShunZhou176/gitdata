#!/usr/bin/env python2
#-*- coding: utf-8 -*-
#@Filename : token_pool.py
#@Date : 2018-04-21-17-12
#@AUTHOR : bai

import Queue

class TokenPool(object):
    def __init__(self):
        self.token_queue_ = Queue.Queue()

    def Init(self, tokens):
        nn = len(tokens)
        if nn == 0:
            print "Token empty"
            return
        for i in range(nn):
            self.token_queue_.put(tokens[i])
    def Return(self, token):
        self.token_queue_.put(token)

    def Get(self):
        return self.token_queue_.get()




# token pool singleton
global_token_pool = TokenPool()
