#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : sikai.zhang
# @Time    : 5/19/19 7:23 PM
from mongoengine import StringField, FloatField, DateTimeField

from core.DBDocument import DBDocument


class SoHuStock(DBDocument):
    code = StringField(required=True)
    cn_name = StringField()
    date = DateTimeField(required=True)  # 日期
    open = FloatField(required=True)  # 开盘价
    close = FloatField(required=True)  # 收盘价
    rise = FloatField(required=True)  # 涨跌额
    rise_rate = FloatField(required=True)  # 涨跌率: %
    lowest = FloatField(required=True)  # 最低
    highest = FloatField(required=True)  # 最高
    trading_volume = FloatField(required=True)  # 成交量
    turnover = FloatField(required=True)  # 成交额: 万
    turnover_rate = FloatField(required=True)  # 换手率: %

    meta = {
        'db_alias': 'stock',
        'strict': False,
    }

    @classmethod
    def create(cls,
               code,
               cn_name,
               date,
               open,
               close,
               rise,
               rise_rate,
               lowest,
               highest,
               trading_volume,
               turnover,
               turnover_rate,
               should_save=True,
               ):
        data = dict(
            code=code,
            cn_name=cn_name,
            date=date,
            open=open,
            close=close,
            rise=rise,
            rise_rate=rise_rate,
            lowest=lowest,
            highest=highest,
            trading_volume=trading_volume,
            turnover=turnover,
            turnover_rate=turnover_rate,
        )
        stock = cls(**data)
        if should_save:
            stock.save()
        return stock
