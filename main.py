#!/usr/bin/env python
# -*- coding:utf8 -*-

"""
Brief: main script

Author: tianxin
Date: 2017/01/08 20:23:45
"""

import argparse
import logging

import spider
import log

def print_usage():
    """Print usage of the script
    """

    print ("Usage: python mini_spider.py -c config_path")

def parse_commandline():
    """Parse config path from command line
    """

    parser = argparse.ArgumentParser(version="1.0.0")
    parser.add_argument("-c", "--config", help="config file path", dest="config_path")
    config_path = parser.parse_args().config_path
    return config_path

def main():
    log.init_log('./log/spider')
    config_path = parse_commandline()

    if config_path is None:
        print_usage()
    else:
        #create a spider and start is   
        _spider = spider.Spider()
        if _spider.initialize(config_path):
            _spider.start()
            _spider.print_info()
            logging.info("All thread finished")
        else:
            logging.error("Initialize spider failed")
            return False

if __name__ == "__main__":
    main()
