# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: sikaizhang
import os
import shutil
from os.path import join
from uuid import uuid4


class WorkSpace(object):
    """
    工作区类

    用处：
    （临时）文件（夹）相关操作，随机名生成，用完后清理
    """

    def __init__(self, sub_dir='', usage='common', base_dir='', create=True):
        # 工作区基本目录、一级目录
        if base_dir:
            self.base_dir = base_dir
        else:
            self.base_dir = os.path.join(os.path.abspath(''), 'rhs_workspace')

        # 工作区类型目录、二级目录
        self.usage_dir = usage
        # 本次工作目录、三级目录
        self.sub_dir = sub_dir or uuid4()
        # 本次工作目录全名
        self.dir = os.path.join(self.base_dir, self.usage_dir, self.sub_dir)

        if create:
            self.create()

    def create(self):
        """创建本次工作目录"""
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

    def rm(self, file_name):
        """在工作目录下删除文件"""
        os.remove(join(self.dir, file_name))

    def clear(self):
        """销毁本次工作目录，包括内部的文件"""
        shutil.rmtree(self.dir, True)

    def pwd(self):
        return self.dir
