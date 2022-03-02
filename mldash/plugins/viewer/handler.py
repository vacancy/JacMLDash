#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# File   : handler.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 09/08/2019
#
# This file is part of JacMLDash.
# Distributed under terms of the MIT license.

import os
from tornado.web import StaticFileHandler
from jacinle.web.app import route


@route(r'/viewer/(.*)')
class FileViewerHandler(StaticFileHandler):
    def initialize(self, path=None, default_filename='index.html'):
        if path is None:
            path = os.getcwd()
        super().initialize(path, default_filename)

    def get_content_type(self) -> str:
        assert self.absolute_path is not None
        if self.absolute_path.endswith('.log'):
            return 'text/plain'
        return super().get_content_type()

