#!/usr/bin/env python
# -*- coding:utf8 -*-

############################################################
# 
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
############################################################
"""
Brief: Crawler_thread

Author: tianxin(tianxin04@baidu.com)
Date: 2017/01/08 20:23:45
"""

import HTMLParser
import urlparse

class PageParser(HTMLParser.HTMLParser):
    """To parse webpage, extract all urls.

    Attributes:
        tag_attr: 带提取的标签属性配置
    """

    def __init__(self):
        #super(PageParser, self).__init__() 这种写法要求PageParser必须是new-style-class, 然而HTMLParser是old-style-class
        HTMLParser.HTMLParser.__init__(self)
        self.candidate_url_list = list() #

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr, value in attrs:
                if attr == 'href':
                    self.candidate_url_list.append(value)

    def extract_urls_from_page(self):
        """axtract all urls from webpage

            Returns: parsed_urls
        """ 
        parsed_urls = []
        for value in self.candidate_url_list:
            try:
                ret = urlparse.urlparse(value)
                if ret.scheme in ("http", "https"):
                    parsed_urls.append(value)
            except Exception as e:
                logging.error("[parse exception]:%s" % e)

        return parsed_urls
