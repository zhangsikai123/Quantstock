#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : sikai.zhang
# @Time    : 5/24/19 9:41 AM
from os.path import join
from os import environ as ENV
import yaml
from mongoengine import connect

_base_dir = join(ENV['root'], 'config')
_db = join(_base_dir, 'database.yaml')

with open(_db, 'r') as yml_file:
    db_configs = yaml.load(yml_file)
    for config in db_configs:
        connect(**config)
