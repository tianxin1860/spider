#!/usr/bin/env python
# -*- coding:utf8 -*-

"""
Brief: CrawlThread

Author: tianxin(15626487296@163.com)
Date: 2017/01/08 20:23:45
"""

import time
import logging
import urllib2
import threading
import socket

import webpage_parse
import webpage_save
import url_table
import encoding_adaptor

class CrawlThread(threading.Thread):
    """CrawlThread class

    Attributes:
        config: Config
        url_queue: Urls to be crawled
        url_set: Urls has been crawld
        max_depth: The maximum depth for crawling
        url_pattern: Regex object
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
        self.url_pattern = config.url_pattern

    def run(self):
        """thread function
        """

        while True:
            url, depth = self.url_queue.get(block=True)

            try:
                response = urllib2.urlopen(url, timeout=self.crawl_timeout)
                page_content = response.read()
            except urllib2.URLError as e:
                logging.error("request of url:%s failed, [Exception]:%s, [Queue_num:%d]" \
                        % (url, e, self.url_queue.qsize()))
                self.url_queue.task_done()
                continue
            except socket.timeout as e:
                logging.error("request of url:%s failed, [Exception]:%s, [Queue_num:%d]" \
                        % (url, e, self.url_queue.qsize()))
                self.url_queue.task_done()
                continue
            except Exception as e:
                logging.error("request of url:%s failed, [Exception]:%s, [Queue_num:%d]" % \
                        (url, e, self.url_queue.qsize()))
                self.url_queue.task_done()
                continue

            # decoding page, return unicode page and encoding of the page
            page, encoding = encoding_adaptor.decode(page_content)

            # save webpage
            webpage_save.save(url, page, encoding, self.save_dir)

            # if depth does not reach max_depth, extract the urls
            if depth < self.max_depth:
                page_parser = webpage_parse.PageParser()
                page_parser.feed(page)
                extracted_urls = page_parser.extract_urls_from_page(url)
                self.add_urls_to_queue(extracted_urls, depth + 1)

            self.url_queue.task_done()

            # 为了防止ip被封禁
            time.sleep(self.crawl_interval)

    def add_urls_to_queue(self, url_list, depth):
        """select url which has not been crawled,
           and matched the url_pattern, 
           and then add these urls to url_queue

            Args:
                url_list:
                depth:
        """
        for url in url_list:
            if not self.url_pattern.match(url):
                logging.info("[url:%s] not satisfied with url_pattehr" % url)
                continue

            if self.url_set.update_set(url) == True:
                self.url_queue.put((url, depth))
