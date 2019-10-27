#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : sikai.zhang
# @Time    : 5/19/19 7:22 PM1
import asyncio
import aiohttp
import ujson as ujson
from models.stock import SoHuStock

isession = None
code_to_name = dict()


def session():
    global isession
    if isession is None:
        isession = aiohttp.ClientSession()

    return isession


def to_url(host, req_body):
    if 'http://' not in host:
        host = 'http://' + host + '/hisHq?'
    body = '/'
    for k, v in req_body.items():
        the_and = '' if body[-1] == '?' else '&'
        body += the_and + (str(k) + '=' + str(v))
    return host + body


async def sohu_stock_collect_data(code):
    # 20110608 --> 20190523
    req_body = dict(
        code=str(code),
        start='20190523',
        end='20190616',
        stat='1',
        order='D',
        period='d',
        callback='historySearchHandler',
        rt='jsonp'
    )
    host = 'q.stock.sohu.com'
    url = to_url(host, req_body)
    print(url)
    async with session().get(to_url(host, req_body)) as resp:
        body = await resp.text()
        body = ujson.loads(body[21:-2])
        if len(body) == 0:
            return {}
        body = body[0]
        body['header'] = ['date', 'open', 'close', 'rise', 'rise_rate', 'lowest', 'highest', 'trading_volume', 'turnover', 'turnover_rate']
        return body

def _deduplicate(data_list):
    res = []
    for data in data_list:
        if SoHuStock.objects(date=data['date'], code=data['code']).first():
            print('find dup %s, %s' % (str(data['date']), data['code']))
            continue
        res.append(data)
    return res


async def do_task(code):
    if not code.startswith('cn_'):
        code = 'cn_' + code
    raw_data = await sohu_stock_collect_data(code)
    header = raw_data.get('header')
    data_list= []
    for data in raw_data.get('hq', []):
        d = {}
        for i in range(len(header)):
            d[header[i]] = data[i]
        d['code'] = code.replace('cn_', '')
        d['cn_name'] = code_to_name[d['code']]
        data_list.append(SoHuStock.create(**d, should_save=False))
    data_list= _deduplicate(data_list)
    if len(data_list) == 0:
        print("no data for %s" % code)
    else:
        SoHuStock.objects().insert(_deduplicate(data_list))
    print('fyeah!')


async def main():
    aws = []
    with open('/Users/zhangsikai/PycharmProjects/StockQuant/seeds', 'r') as f:
        for l in f:
            raw_code = l[:6]
            code = 'cn_' + l[:6]
            name = l[6:l.find("股吧资金流数据")].strip(' ').strip('    ').strip('\t')
            code_to_name[raw_code] = name
            aws.append(do_task(code))
    await asyncio.gather(*aws)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
