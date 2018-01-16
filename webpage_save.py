#!/usr/bin/env python
# -*- coding:utf8 -*-

"""
Brief: Save webpage to specified directory

Author: tianxin(15626487296@163.com)
Date: 2017/01/08 20:23:45
"""

import os
import urllib

import logging

def save(url, page, encoding, save_dir):
    """save webpage to the specified directory

        Args:
            url: use url as file name of the saved webpage
            page: html page
            encoding: save page with the encoding
            save_dir: output directory
    """ 

    file_path = os.path.join(save_dir, urllib.quote_plus(url))

    try:
        if isinstance(page, unicode) and encoding is not None:
            encode_page = page.encode(encoding)
        else:
            logging.warn("[url:%s] page encoding is not unicode" % url)
            encode_page = page
    except UnicodeEncodeError as e:
        logging.error("[Exception:] %s" % e)
        encode_page = page

    try:
        with open(file_path, 'wt') as file:
            file.write(encode_page)
            file.flush()
    except IOError as e:
        logging.error("[url:%s] save failed, Exception:%s" % (url, e))
