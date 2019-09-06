#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# File   : local_storage.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 05/25/2019
#
# This file is part of JacMLDash.
# Distributed under terms of the MIT license.

import os.path as osp
from .utils import safe_dump



class ProjectStorage(object):
    def __init__(self):
        self.experiments = dict()

    def save(self):


class LocalStorageManager(object):
    def __init__(self, global_configs):
        self.global_configs = global_configs
        self.project_configs = dict()

        for proj_spec in self.global_configs['projects']:
            self.load_project(proj_spec)

    def load_project(self, proj_spec):
        name = proj_spec['name']
        path = proj_spec['path']

        proj_file = osp.join(path, 'jacmldash.pkl')
        io.load()

