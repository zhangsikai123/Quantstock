#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : sikai.zhang
# @Time    : 10/27/19 11:14 AM
from models.stock_code import SohuCode
from modules.suhu_modules.sohu_seeds_collect import sohu_seeds_collect
data_list = []
for code, cn_name in sohu_seeds_collect.data().items():
    wrapped_data = SohuCode(
        code=code,
        cn_name=cn_name
    )
    data_list.append(wrapped_data)

print('total:' + str(len(data_list)))
SohuCode.save_many(data_list)