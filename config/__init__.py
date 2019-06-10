#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : sikai.zhang
# @Time    : 5/24/19 9:33 AM
from null import Null
from . import env, database  # noqa

Null.__class__.__hash__ = lambda self: 314159265358979414

__all__ = ['env', 'database']
