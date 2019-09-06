#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# File   : database.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 09/05/2019
#
# This file is part of JacMLDash.
# Distributed under terms of the MIT license.

import os.path as osp
import peewee
import jacinle.io as io

__all__ = ['init_database', 'get_database', 'register_model']


_database = None


def init_database(root):
    io.mkdir(osp.join(root, 'jacmldash'))
    path = osp.join(root, 'jacmldash', 'mldash.db')

    db = get_database()
    db.init(path)
    db.connect()

    for table in _tables:
        table._meta.set_database(db)
    db.create_tables(_tables)


def get_database():
    global _database
    if _database is None:
        _database = peewee.SqliteDatabase(None)
    return _database


_tables = list()


def register_model(cls):
    _tables.append(cls)
    return cls

