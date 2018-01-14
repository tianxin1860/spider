#!/usr/bin/env python
# -*- coding:utf8 -*-

"""
Brief: Crawler_thread

Author: tianxin
Date: 2017/01/08 20:23:45
"""

import urllib2
import threading
import socket

import logging
import webpage_parse
import webpage_save
import url_table
import encoding_adaptor

class CrawlThread(threading.Thread):
    """CrawlThread class

    Attributes:
        config: config
        url_queue: urls to be crawled
        url_set: urls has been crawld
        max_depth: The maximum depth for crawling
        crawl_interval: The interval for crawling
        crawl_timeout: The max time waiting for crawling
    """

    def __init__(self, config, url_queue, url_set):
        """initialize object of CrawlThread

            Args:
                config: spider's config
                url_queue: object of Queue storing all urls to be crawled
        """
        super(CrawlThread, self).__init__()
        self.url_queue = url_queue
        self.url_set = url_set
        self.max_depth = config.max_depth
        self.crawl_interval = config.crawl_interval
        self.crawl_timeout = config.crawl_timeout
        self.save_dir = config.save_dir

    def run(self):
        """thread function
        """
        while True:
            finish_flag, page, depth, url = self.download()
            if finish_flag:
                break
            elif not finish_flag and page is not None:
                page, encoding = encoding_adaptor.decode(page)
                if encoding is None:
                    continue #对于未识别出编码类型的资源,例如安装包等资源,直接跳过
                if depth < self.max_depth:
                    webpage_save.save(url, page, encoding, self.save_dir) #此处url需要考虑重新组织
                    page_parser = webpage_parse.PageParser()
                    page_parser.feed(page)
                    extracted_urls = page_parser.extract_urls_from_page()
                    self.add_urls_to_queue(extracted_urls, depth + 1)
                elif depth == self.max_depth:
                    webpage_save.save(url, page, encoding, self.save_dir)
                else:
                    continue
            else:
                continue
    
    def download(self):
        """download html code of the url
        """
        try:
            url, depth = self.url_queue.get()
        except Queue.Empty as e:
            logging.info("crawling finished in thread:%s, Exception:%s" % (self.getName(), e))
            return True, None, -1, url

        if depth > self.max_depth:
            logging.info("[Thread:%s] skip url:%s depth > max_depth" % self.getName(), url)
            self.url_queue.task_done()
            return False, None, depth, url

        try:
            response = urllib2.urlopen(url, timeout=self.crawl_timeout)
            page_content = response.read()
            self.url_queue.task_done()
            return False, page_content, depth, url
        except urllib2.URLError as e:
            logging.error("request of url:%s failed, [Exception]:%s, [Queue_num:%d]" % (url, e, self.url_queue.qsize()))
            self.url_queue.task_done()
            return False, None, depth, url
        except socket.timeout as e:
            logging.error("request of url:%s failed, [Exception]:%s, [Queue_num:%d]" % (url, e, self.url_queue.qsize()))
            self.url_queue.task_done()
            return False, None, depth, url
        except Exception as e:
            logging.error("request of url:%s failed, [Exception]:%s, [Queue_num:%d]" % (url, e, self.url_queue.qsize()))
            self.url_queue.task_done()
            return False, None, depth, url

    def add_urls_to_queue(self, url_list, depth):
        """
            select url which has not been crawled,
            and then add these urls to url_queue

            Args:
                url_list:
                depth:
        """
        for url in url_list:
            if self.url_set.update_set(url) == "OK":
                self.url_queue.put((url, depth))
