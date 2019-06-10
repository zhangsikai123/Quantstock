#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : sikai.zhang
# @Time    : 5/19/19 7:22 PM
import json
import requests
import ujson as ujson


def to_url(host, req_body):
    if 'http://' not in host:
        host = 'http://' + host + '/hisHq?'
    body = '/'
    for k, v in req_body.items():
        the_and = '' if body[-1] == '?' else '&'
        body += the_and + (str(k) + '=' + str(v))
    return host + body


def sohu_stock_collect_data(code):
    # 20110608 --> 20190523
    req_body = dict(
        code=code,
        start='19000930',
        end='20190523',
        stat='1',
        order='D',
        period='d',
        callback='historySearchHandler',
        rt='jsonp'
    )
    host = 'q.stock.sohu.com'
    url = to_url(host, req_body)
    print(url)
    response = requests.get(to_url(host, req_body))
    body = response.text
    body = ujson.loads(body[21:-2])[0]
    return len(body['hq'])

def task(args):
    for a in args:
        print(a)


if __name__ == '__main__':
    with open('/Users/zhangsikai/PycharmProjects/StockQuant/seeds', 'r') as f:
        for l in f:
            code = l[:6]
            sohu_stock_collect_data(code)

