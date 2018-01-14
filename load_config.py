#!/usr/bin/env python
# -*- coding:utf8 -*-

"""
Brief: load config

Author: tianxin
Date: 2017/01/08 20:23:45
"""
import os
import ConfigParser

import log

class Config(object):
    """load config

    Attributes:
        config_parser: ConfigParser object
        config_path:
        seed_file: seed url file path
        save_dir: The path webpages are saved in
        max_depth: The max depth for crawling
        crawl_interval: The interval of crawling
        crawl_timeout: The max wait length of time of crawling.
        thread_num: number of crawling thread
    """

    def __init__(self, config_path):
        """
            Args:
                config_path: config file's absolute path
        """
        self.config_parser = ConfigParser.ConfigParser()
        self.config_path = config_path

    def load_config(self):
        """Load config to Config object
            
            Args:
                None

            Returns:
                True: if load config file successfully return True
                False: if load config file failed return False
        """
        if not os.path.exists(self.config_path):
            logging.error("%s does not exist" % self.config_path)
            return False
        else:
            try:
                self.config_parser.read(self.config_path)
            except ConfigParser.ParsingError as e:
                logging.error("config parse error: %s" % e)
                return False
            try:
                self.seed_file = self.config_parser.get("spider", "seed_file")
                self.save_dir = self.config_parser.get("spider", "save_dir")
                self.max_depth = self.config_parser.getint("spider", "max_depth")
                self.crawl_interval = self.config_parser.getint("spider", "crawl_interval")
                self.crawl_timeout = self.config_parser.getint("spider", "crawl_timeout")
                self.thread_num = self.config_parser.getint("spider", "thread_num")
                return True
            except ConfigParser.NoSectionError as e:
                logging.error("[Exception]: %s" % e)
                return False
            except ConfigParser.NoOptionError as e:
                logging.error("[Exception]: %s" % e)
                return False
            except Exception as e:
                logging.error("[Exception]: %s" % e)
                return False
