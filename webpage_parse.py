#!/usr/bin/env python
# -*- coding:utf8 -*-

"""
Brief: PageParser

Author: tianxin(15626487296@163.com)
Date: 2017/01/08 20:23:45
"""

import HTMLParser
import urlparse

class PageParser(HTMLParser.HTMLParser):
    """To parse webpage, extract all urls.

        Attrbutes:
            candidate_url_list: candidate urls which will be selected to crwal
    """

    def __init__(self):
        #super(PageParser, self).__init__() 这种写法要求PageParser必须是new-style-class, 然而HTMLParser是old-style-class
        HTMLParser.HTMLParser.__init__(self)
        self.candidate_url_list = list()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr, value in attrs:
                if attr == 'href':
                    self.candidate_url_list.append(value)

    def extract_urls_from_page(self, base_url):
        """extract all urls from webpage

            Args:
                base_url: url corresponding to the webpage

            Returns: parsed_urls
        """ 
        parsed_urls = list()
        for value in self.candidate_url_list:
            try:
                ret = urlparse.urlparse(value)
                if ret.scheme in ("http", "https"):
                    parsed_urls.append(value)
                elif ret.scheme == '':
                    url = urlparse.urljoin(base_url, value)
                    parsed_urls.append(url)
                else:
                    continue
            except Exception as e:
                logging.error("[parse exception]:%s" % e)

        return parsed_urls
