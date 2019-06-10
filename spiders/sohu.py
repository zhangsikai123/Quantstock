#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : sikai.zhang
# @Time    : 5/19/19 7:22 PM1
from multiprocessing.pool import Pool

import requests
import ujson as ujson

from mongoengine import get_db

from models.stock import SoHuStock


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
        code=str(code),
        start='19000523',
        end='20190606',
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
    body['header'] = ['date', 'open', 'close', 'rise', 'rise_rate', 'lowest', 'highest', 'trading_volume',
                      'turnover', 'turnover_rate']
    return body


def _dedup(datas):
    res = []
    for data in datas:
        if SoHuStock.objects(date=data['date'], code=data['code']).first():
            print('find dup %s, %s' % (str(data['date']), data['code']))
            continue
        res.append(data)
    return res


def task(codes):
    datas = []
    for code in codes:
        if not code.startswith('cn_'):
            code = 'cn_' + code
        raw_data = sohu_stock_collect_data(code)
        header = raw_data.get('header')
        for data in raw_data.get('hq', []):
            d = {}
            for i in range(len(header)):
                d[header[i]] = data[i]
            d['code'] = code
            datas.append(SoHuStock.create(**d, should_save=False))
    SoHuStock.objects().insert(_dedup(datas))


if __name__ == '__main__':
    batches = []
    batch_size = 100
    batch = []
    with open('/Users/zhangsikai/PycharmProjects/StockQuant/seeds', 'r') as f:
        for l in f:
            code = 'cn_' + l[:6]
            batch.append(code)
            if len(batch) == batch_size:
                batches.append(batch)
                batch = []

    p = Pool(32)
    datas = p.map(task, batches)

    print(len(datas))
    SoHuStock.objects().insert(datas)
