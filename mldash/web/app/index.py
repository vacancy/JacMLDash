#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# File   : index.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 10/23/2018
#
# This file is part of Jacinle.
# Distributed under terms of the MIT license.

from jacweb.web import route, JacRequestHandler
from mldash.data.orm import init_database, ProjectMetainfo, Desc


@route(r'/')
class IndexHandler(JacRequestHandler):
    def get(self):
        metainfo = ProjectMetainfo.get_all()
        descs = Desc.select().execute()
        kwargs = {'metainfo': metainfo, 'title': metainfo['title'], 'descs': descs}
        self.render('index.html', **kwargs)

