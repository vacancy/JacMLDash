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
import shutil
import peewee
import jacinle
import jacinle.io as io

__all__ = ['init_database', 'get_database', 'register_model', 'migrate_database', 'migrate_1_1', 'get_latest_version']


logger = jacinle.get_logger(__file__)
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

    from .project import init_project
    init_project()

    migrate_database(db, path)


def get_database():
    global _database
    if _database is None:
        _database = peewee.SqliteDatabase(None)
    return _database


_tables = list()


def register_model(cls):
    _tables.append(cls)
    return cls


def migrate_database(db, path):
    from mldash.orm.project import ProjectMetainfo
    key_values = ProjectMetainfo.get_all()

    if 'dbversion' in key_values:
        ver = key_values['dbversion']
    else:
        ver = '1.0'

    if ver != get_latest_version():
        shutil.copyfile(path, path + '.' + ver)
        if ver == '1.0':
            ver = migrate_1_1(db)
        ProjectMetainfo.update('dbversion', ver)


def migrate_1_1(db):
    logger.warning('Migrating the database from version 1.0 to 1.1')
    from playhouse.migrate import migrate, SqliteMigrator
    migrator = SqliteMigrator(db)
    extra_info = peewee.TextField(null=True)
    migrate(
        migrator.add_column('Desc', 'extra_info', extra_info),
        migrator.add_column('Experiment', 'extra_info', extra_info)
    )
    return '1.1'


def get_latest_version():
    return '1.1'

