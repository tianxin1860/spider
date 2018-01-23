#!/usr/bin/env python
# -*- coding:utf8 -*-

"""
Brief: test load_config module

Author: tianxin(15626487296@163.com)
Date: 2017/01/08 20:23:45
"""

import sys
import unittest

sys.path.append("../../spider")

import load_config

class TestLoadConfig(unittest.TestCase):
    """ Unittest for load_config module
    """

    def setUp(self):
        """ set config file path for test
        """

        self.config = load_config.Config("./conf/spider.conf")

    def test_load_config(self):
        """ test load_config function
        """

        # Test when load config successfully
        self.assertTrue(self.config.load_config())

        # Test when config file does not exist
        self.config.config_path = "fake path for test"
        self.assertFalse(self.config.load_config())

if __name__ == "__main__":
    unittest.main()
