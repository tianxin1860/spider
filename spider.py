#!/usr/bin/env python
# -*- coding:utf8 -*-

############################################################
# 
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
############################################################
"""
Brief: spider

Author: tianxin(tianxin04@baidu.com)
Date: 2017/01/08 20:23:45
"""

import Queue
import threading
import logging

import load_seed_file
import load_config
import url_table
import crawl_thread

class Spider(object):
    """Spider class

    Attributes:
        url_queue: urls that wait to be crawled
        url_set: urls that have been crawled
        config: config object
    """

    def __init__(self):
        self.url_queue = Queue.Queue()
        self.url_set = url_table.ThreadSafeSet()


    def initialize(self, config_path):
        """initialize url_queue and load config file.
            Args:
                config_path: config file path

            Returns:
                True: initialize succeed
                False: initialsze failed
        """

        self.config = load_config.Config(config_path)
        ret = self.config.load_config()
        if not ret:
            logging.error("load config file failed")
            return False

        seed_urls = load_seed_file.get_seed_urls(self.config.seed_file)
        if seed_urls is None:
            logging.error("load seed file failed")
            return False

        for url in seed_urls:
            if self.url_set.update_set(url) == "OK":
                self.url_queue.put((url, 0))

        return True


    def start(self):
        """create crawl thread and start crawling
        """

        for i in range(self.config.thread_num):
            thread = crawl_thread.CrawlThread(self.config, self.url_queue, self.url_set)
            thread.daemon = True
            thread.start()

        self.url_queue.join()

    def print_info(self):
        """Print statistics information
        """
        logging.info("[crawled num:%d]" % self.url_set.size())
