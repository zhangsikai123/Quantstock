#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : sikai.zhang
# @Time    : 10/27/19 11:15 AM
from mongoengine import StringField
from core.DBDocument import DBDocument


class SohuCode(DBDocument):
    code = StringField(required=True)
    cn_name = StringField()

    meta = {
        'db_alias': 'stock',
        'strict': False,
    }
