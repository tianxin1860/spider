#!/usr/bin/env python
# -*- coding:utf8 -*-

"""
Brief: handle all things that related to encoding

Author: tianxin
Date: 2017/01/08 20:23:45
"""

def decode(webpage):
    """decode webpage with different encoding to unicode

        Args:
            webpage: content of webpage which encoding might be
                     utf-8, gbk, gb18030, gb2312 and so on

        Returns:
            decode_webpage: unicode webpage
            encoding: encoding of the webpage
    """
    encodings = ["utf-8", "gbk", "gb18030", "gb2312"]
    for encoding in encodings:
        try:
            decode_webpage = webpage.decode(encoding)
            return decode_webpage, encoding
        except UnicodeDecodeError as e:
            continue
    return webpage, None
