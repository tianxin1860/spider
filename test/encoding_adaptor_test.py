#!/usr/bin/env python
# -*- coding:utf8 -*-

"""
Brief: UnitTest for encoding_adaptor module

Author: tianxin(15626487296@163.com)
Date: 2017/01/08 20:23:45
"""

import sys
import unittest

sys.path.append("../../spider")

import encoding_adaptor

class TestEncodingAdaptor(unittest.TestCase):
    """ unittest for encoding adaptor module
    """

    def setUp(self):
        """construct webpage for test
        """

        self.webpage = u"人生苦短,I love python"
        self.encoding = ["utf-8", "gbk"]

    def test_decode(self):
        """ test decode function
        """

        # Test when webpage's encoding is utf-8/gbk/gb18030/gb2312
        for encoding in self.encoding:
            encode_webpage = self.webpage.encode(encoding)
            decode_webpage, webpage_encoding = encoding_adaptor.decode(encode_webpage)
            self.assertTrue(isinstance(decode_webpage, unicode))
            print encoding
            print webpage_encoding
            self.assertTrue(encoding == webpage_encoding)

if __name__ == "__main__":
    unittest.main()
