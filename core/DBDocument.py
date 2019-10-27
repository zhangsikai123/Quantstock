#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Mr.Cypress
# @Time    : 2018/11/28 7:24 PM
from collections import defaultdict
from mongoengine import Document, DateTimeField
from datetime import datetime
BEFORE_SAVE_HOOK = 'before_save'
AFTER_SAVE_HOOK = 'after_save'


class DBDocument(Document):
    meta = {
        'db_alias': 'stock',
        'abstract': True,
        'strict': False,
    }

    create_time = DateTimeField(default=datetime.utcnow)
    BEFORE_SAVE_HOOKS = [BEFORE_SAVE_HOOK]
    AFTER_SAVE_HOOKS = [AFTER_SAVE_HOOK]

    @property
    def string_id(self):
        return str(self.id)

    def _call_self_hooks(self, *hooks):
        for hook in hooks:
            if hasattr(self, hook) and callable(getattr(self, hook)):
                getattr(self, hook)()

    def _call_all_super_obj_hooks(self, *hooks):
        for super_class in self.__class__.__mro__:
            super_obj = super(super_class, self)
            for hook in hooks:
                if hasattr(super_obj, hook) and callable(getattr(super_obj, hook)):
                    getattr(super_obj, hook)()

    def save(self, *args, **kwargs):
        self._call_self_hooks(*self.BEFORE_SAVE_HOOKS)
        self._call_all_super_obj_hooks(*self.BEFORE_SAVE_HOOKS)
        super(DBDocument, self).save(*args, **kwargs)
        self._call_self_hooks(*self.AFTER_SAVE_HOOKS)
        self._call_all_super_obj_hooks(*self.AFTER_SAVE_HOOKS)

    def hard_delete(self):
        self.delete()

    @classmethod
    def get_by_id(cls, _id):
        return cls.objects(id=_id).first()

    @classmethod
    def get_by_ids(cls, ids):
        """
        return a Cursor!
        :param ids:
        """
        return cls.objects(id__in=ids)

    @classmethod
    def get_by_query(cls, query=None):
        if not query:
            # 兼容query为None的情况
            query = {}
        return cls.objects(**query)

    @classmethod
    def get_enable_by_query(cls, query=None):
        if not query:
            query = {}
        if hasattr(cls, 'enabled') and 'enabled' not in query:
            # 如果query中传入enabled，则以传入参数为准
            query['enabled'] = True
        return cls.objects(**query)

    @classmethod
    def save_many(cls, documents):
        if not documents or len(documents) == 0:
            return
        return cls.objects.insert(documents)

    @classmethod
    def create_by_data(cls, **kwargs):
        """
        kwargs中
        key值为继承该类的document的所有field
        """
        save = kwargs.pop('save', None)
        doc = cls(**kwargs)
        if save is False:
            return doc
        doc.save()
        return doc

    def update_by_data(self, **kwargs):
        """
        kwargs中
        key值为继承该类的document的所有field
        """
        self.update(**kwargs)
        self.reload()

    @classmethod
    def load_by(cls, query, group_by=None, field_only=None, enabled=False):
        """
        load by 方法返回map
        group_by 存在的时候使用 group_by {field}
        field_only 存在，value 为 doc.field
        """
        if group_by:
            assert isinstance(group_by, str)
            assert hasattr(cls, group_by)
        if field_only:
            assert isinstance(field_only, str)
            assert hasattr(cls, field_only)
        if enabled:
            result_list = cls.get_enable_by_query(query)
        else:
            result_list = cls.get_by_query(query)
        if not group_by:
            return {data.string_id: data for data in result_list}

        result_map = defaultdict(list)
        for data in result_list:
            value = data
            if field_only:
                value = getattr(data, field_only)
            result_map[getattr(data, group_by)].append(value)
        return result_map

    @classmethod
    def load_enable_by(cls, query, group_by=None, field_only=None):
        return cls.load_by(query, group_by, field_only, enabled=True)

    @classmethod
    def get_one(cls):
        """返回第一个"""
        return cls.get_by_query({}).first()

    @classmethod
    def get_enabled_one(cls):
        """返回第一个"""
        return cls.get_enable_by_query({}).first()
