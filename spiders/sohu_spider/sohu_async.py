#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : sikai.zhang
# @Time    : 8/4/19 9:33 PM
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : sikai.zhang
# @Time    : 5/19/19 7:22 PM1

from multiprocessing.pool import Pool
from models.stock import SoHuStock
from modules.suhu_modules.sohu_seeds_collect import sohu_seeds_collect
from modules.suhu_modules.sohu_stock_search import SohuStockSearch
from logger import logger
code_to_name = dict()


# 20110608 --> 20190523
def _deduplicate(data_list):
    logger.info('start deduplicate ..., total data {}'.format(len(data_list)))
    res = []
    for data in data_list:
        if SoHuStock.get_by_query(dict(date=data['date'], code=data['code'])).first():
            logger.info('find dup %s, %s' % (str(data['date']), data['code']))
            continue
        res.append(data)
    return res


def task(codes):
    data_list= []
    for code in codes:
        raw_data = SohuStockSearch.search_stock_data('20190524', '20190802', code)
        header = raw_data.get('header')
        for data in raw_data.get('hq', []):
            d = {}
            for i in range(len(header)):
                d[header[i]] = data[i]
            d['cn_name'] = sohu_seeds_collect.get_stock_info(code=code)
            d['code'] = code
            data_list.append(SoHuStock.create(**d, should_save=False))
    logger.info('BATCH DONE')
    return data_list


if __name__ == '__main__':
    batches = []
    batch_size = 100
    batch = []
    codes = sohu_seeds_collect.data().keys()
    for code in codes:
        batch.append(code)
        if len(batch) == batch_size:
            batches.append(batch)
            batch = []

    p = Pool(32)
    data_list= p.map(task, batches)
    all = []
    for data in data_list:
        all.extend(data)

    logger.info('Start writing {} data to disk ...'.format(len(all)))
    SoHuStock.save_many(_deduplicate(all))

    logger.info('DONE')
