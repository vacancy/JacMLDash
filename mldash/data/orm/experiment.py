#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# File   : experiment.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 09/05/2019
#
# This file is part of JacMLDash.
# Distributed under terms of the MIT license.

from datetime import datetime
import peewee
from .database import register_model
import jacinle.io as io


class ModelWithCUTime(peewee.Model):
    create_time = peewee.DateTimeField("%Y-%m-%d %H:%M:%S", default=datetime.now)
    update_time = peewee.DateTimeField("%Y-%m-%d %H:%M:%S", default=datetime.now)

    def save(self, *args, **kwargs):
        if self.get_id() is None:
            self.create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return super().save(*args, **kwargs)


@register_model
class Desc(ModelWithCUTime):
    desc_name = peewee.CharField(unique=True)
    desc_description = peewee.TextField(default='')
    desc_notes = peewee.TextField(default='')
    metrics = peewee.TextField(null=True)


@register_model
class Experiment(ModelWithCUTime):
    desc = peewee.ForeignKeyField(Desc, backref='exprs')
    expr_name = peewee.CharField()
    expr_description = peewee.TextField(default='')
    expr_notes = peewee.TextField(default='')
    metrics = peewee.TextField(null=True)

    class Meta:
        indexes = [(('desc', 'expr_name'), True)]


@register_model
class Run(ModelWithCUTime):
    expr = peewee.ForeignKeyField(Experiment, backref='runs')
    run_name = peewee.CharField(index=True)
    run_description = peewee.TextField(default='')
    run_notes = peewee.TextField(default='')

    command = peewee.TextField()
    args = peewee.TextField()
    configs = peewee.TextField()
    highlight_args = peewee.TextField()
    highlight_configs = peewee.TextField()

    metainfo_file = peewee.TextField(null=True)
    log_file = peewee.TextField(null=True)
    meter_file = peewee.TextField(null=True)
    tb_dir = peewee.TextField(null=True)
    extra_info = peewee.TextField(null=True)
    metrics = peewee.TextField(null=True)

    is_master = peewee.BooleanField(default=True)
    refer = peewee.ForeignKeyField('self', null=True, backref='referee')

    class Meta:
        indexes = [(('expr', 'run_name'), True)]

    _extra_info_dict_cache = None

    @property
    def extra_info_dict(self):
        if self._extra_info_dict_cache is None:
            if self.extra_info is None or self.extra_info == '':
                self._extra_info_dict_cache = dict()
            else:
                self._extra_info_dict_cache = io.loads_json(self.extra_info)
        return self._extra_info_dict_cache

    def update_extra_info(self):
        self.extra_info = io.dumps_json(self.extra_info_dict)

