#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# File   : index.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 10/23/2018
#
# This file is part of Jacinle.
# Distributed under terms of the MIT license.

import json
from jacinle.web.app import route, JacRequestHandler
from mldash.data.orm import ProjectMetainfo, Desc
from mldash.web.ui_methods import get_ui_methods
from mldash.web.custom_pages import get_custom_pages


@route(r'/')
class IndexHandler(JacRequestHandler):
    def get(self):
        metainfo = ProjectMetainfo.get_all()
        descs = Desc.select().execute()
        kwargs = {'metainfo': metainfo, 'title': metainfo['title'], 'desc_groups': self.group_descs(descs), 'custom_pages': get_custom_pages()}

        self.render('index.html', **kwargs)

    def group_descs(self, descs):
        ui_methods = get_ui_methods()
        group = dict()
        for desc in reversed(descs):
            group_name, desc_name = ui_methods.split_group_name(self, desc.desc_name)
            group.setdefault(group_name, dict())[desc_name] = desc
        return group


@route(r'/api/search-list')
class APISearchListHandler(JacRequestHandler):
    def get(self):
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')

        descs = Desc.select().execute()
        outputs = list()
        for desc in descs:
            outputs.append(f'#desc/{desc.desc_name}')
        for desc in descs:
            for expr in desc.exprs:
                outputs.append(f'#desc/{desc.desc_name}/expr/{expr.expr_name}')
        for desc in descs:
            for expr in desc.exprs:
                for run in expr.runs:
                    outputs.append(f'#desc/{desc.desc_name}/expr/{expr.expr_name}/run/{run.run_name}')
        self.write(json.dumps(outputs))

