#!/usr/bin/env python
# -*- coding:utf8 -*-

"""
Brief: 实现线程安全的集合类

Author: tianxin
Date: 2017/01/08 20:23:45
"""

import threading

class ThreadSafeSet(object):
    """线程安全的集合类，用于保存已经抓取的url，用来去重

    Attributes:
        __safe_set: thread safety set
    """

    def __init__(self):
        self.__safe_set = set()
        self.__lock = threading.Lock()

    def size(self):
        return len(self.__safe_set)

    def update_set(self, url):
        """Add url to __safe_set

            Args:
                url: url to add to set

            Returns:
                "OK"   : If url has been added to set successfully
                "ERROR": If url has existed in set
        """
        self.__lock.acquire()
        if url in self.__safe_set:
            ret = "ERROR"
        else:
            self.__safe_set.add(url)
            ret = "OK"
        self.__lock.release()
        return ret
