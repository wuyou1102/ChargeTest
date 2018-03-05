# -*- encoding:UTF-8 -*-
__author__ = 'wuyou'
from time import time, localtime, strftime

class TimeFormat(object):
    __FORMAT = '%Y_%m_%d-%H_%M_%S'
    __TEST_FMT = '%H:%M:%S'

    @staticmethod
    def set_time_format(time_format):
        TimeFormat.__FORMAT = time_format

    @staticmethod
    def get_time_format():
        return TimeFormat.__FORMAT

    @staticmethod
    def timestamp():
        return strftime(TimeFormat.__FORMAT, localtime(time()))

    @staticmethod
    def test_timestamp():
        return strftime(TimeFormat.__TEST_FMT, localtime(time()))

    @staticmethod
    def time():
        return time()

    @staticmethod
    def data_stamp():
        return strftime('%m%d', localtime(time()))

if __name__ == '__main__':
    TimeFormat.set_time_format('%m-%d =%H:%M:%S')
    for x in range(10):
        TimeFormat.set_time_format('%m-%d =%H:%M:%S'+str(x))
        print TimeFormat.timestamp()
    print TimeFormat().get_time_format()