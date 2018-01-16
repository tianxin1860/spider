#!/usr/bin/env python
# -*- coding:utf8 -*-

"""
Brief: load seed url from sedd file

Author: tianxin(15626487296@163.com)
Date: 2017/01/08 20:23:45
"""

import os.path
import logging

def get_seed_urls(seed_file):
    """Load seed urls from seed_file into queue and set depth=0.

    Args:
        seed_file: absolute path of seed_file

    Returns:
        urls_to_be_crawl: A Queue object that stores the seed urls in seed_file.

        None object: if get_seed_urls failed, then return a None object.
    """
    if not os.path.isfile(seed_file):
        logging.error("%s not found" % seed_file)
        return None

    urls_to_be_crawl = set()
    with open(seed_file) as f:
        for line in f:
            if line.strip() == "":
                continue
            else:
                url = line.strip()
                urls_to_be_crawl.add(url)
        return  urls_to_be_crawl
