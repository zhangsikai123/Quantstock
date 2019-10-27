#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : sikai.zhang
# @Time    : 8/2/19 11:40 PM
import os


class SohuSeedsCollect(object):
    __code_to_stock = dict()

    def __init__(self):
        resources = os.path.dirname(os.path.realpath('.'))
        with open(resources + '/modules/resources/seeds', 'r') as f:
            for l in f:
                code = 'cn_' + l[:6]
                name = l[6:l.find("股吧资金流数据")].strip(' ').strip('    ').strip('\t')
                self.__code_to_stock[code] = dict(name=name)

    def get_stock_info(self, code):
        return self.__code_to_stock[code]

    def data(self):
        return self.__code_to_stock


sohu_seeds_collect = SohuSeedsCollect()