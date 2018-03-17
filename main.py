#!/usr/bin/env python
# -*- coding:utf8 -*-

"""
Brief: main script

Author: tianxin(15626487296@163.com)
Date: 2017/01/08 20:23:45
"""

import argparse
import logging

import spider
import log

def print_usage():
    """Print usage of the script
    """

    print ("Usage: python main.py -c config_path")


def parse_commandline():
    """Parse config path from command line
    """
    parser = argparse.ArgumentParser(version="1.0.0")
    parser.add_argument("-c", "--config", help="config file path for spider", dest="config_path")
    config_path = parser.parse_args().config_path
    return config_path


def main():
    """1.初始化日志
       2.解析命令行参数获取配置文件路径
       3.创建Spider对象并初始化
       4.开始抓取
    """
    log.init_log('./log/spider')
    config_path = parse_commandline()

    if config_path is None:
        print_usage()
    else:
        #create a spider and start it 
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
