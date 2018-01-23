#!/usr/bin/env python
# -*- coding:utf8 -*-

"""
Brief: UnitTest for load_seed_file module

Author: tianxin(15626487296@163.com)
Date: 2017/01/08 20:23:45
"""

import sys
import unittest

sys.path.append("../../spider")

import load_seed_file

class TestLoadSeedFile(unittest.TestCase):
    """ unittest for load_seed_file module
    """

    def test_get_seed_urls(self):
        """ test get_seed_urls function
        """

        # Test when seed file exist and not empty
        seed_file = "./conf/valid_seed_file"
        url_set = load_seed_file.get_seed_urls(seed_file)
        self.assertTrue(len(url_set) > 0)

        # Test when seed file is empty
        seed_file = "./conf/empty_seed_file"
        url_set = load_seed_file.get_seed_urls(seed_file)
        self.assertTrue(len(url_set) == 0)

        # Test when seed file does not exist
        seed_file = "./conf/not_exist_seed_file"
        url_set = load_seed_file.get_seed_urls(seed_file)
        self.assertTrue(url_set is None)

if __name__ == "__main__":
    unittest.main()
