#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : sikai.zhang
# @Time    : 8/2/19 11:24 PM
import ujson
import requests
from core.ExceptionHandler import ModuleException
from logger import logger


class SohuStockSearch(object):

    @classmethod
    def __to_url(cls, host, query_body):
        if 'http://' not in host:
            host = 'http://' + host + '/hisHq?'
        body = '/'
        for k, v in query_body.items():
            the_and = '' if body[-1] == '?' else '&'
            body += the_and + (str(k) + '=' + str(v))
        return host + body

    @classmethod
    def search_stock_data(cls, start, end, code):
        """search stock data by start and end date"""
        if start > end:
            raise ModuleException("start {} should be smaller than end {}".format(
                start, end
            ))
        query_body = dict(
            code=str(code),
            start=start,
            end=end,
            stat='1',
            order='D',
            period='d',
            callback='historySearchHandler',
            rt='jsonp'
        )
        host = 'q.stock.sohu.com'
        url = cls.__to_url(host, query_body)
        logger.info('start query {}'.format(url))
        response = requests.get(cls.__to_url(host, query_body))
        body = response.text
        body = ujson.loads(body[21:-2])
        if len(body) == 0:
            return {}
        body = body[0]
        body['header'] = ['date', 'open', 'close', 'rise', 'rise_rate', 'lowest', 'highest', 'trading_volume',
                          'turnover', 'turnover_rate']
        logger.info('query {} done'.format(url))

        return body

    @classmethod
    async def async_search_stock_data(cls, start, end, code):
        return cls.search_stock_data(start, end, code)
