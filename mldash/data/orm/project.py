#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# File   : project.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 09/05/2019
#
# This file is part of JacMLDash.
# Distributed under terms of the MIT license.

import os
import os.path as osp
from datetime import datetime
import peewee
from .database import register_model


@register_model
class ProjectMetainfo(peewee.Model):
    key = peewee.CharField(unique=True)
    value = peewee.TextField()

    @classmethod
    def get_all(cls):
        metainfo = dict()
        for item in cls.select():
            metainfo[item.key] = item.value
        return metainfo

    @classmethod
    def set_all(cls, metainfo):
        for key, value in metainfo.items():
            cls.replace(key=key, value=value).execute()

    @classmethod
    def update(cls, key, value):
        cls.replace(key=key, value=value).execute()


def init_project():
    if len(ProjectMetainfo.get_all()) == 0:
        ProjectMetainfo.set_all({
            'title': osp.basename(os.getcwd()),
            'create_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

