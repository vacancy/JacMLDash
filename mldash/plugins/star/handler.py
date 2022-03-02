#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# File   : handler.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 09/08/2019
#
# This file is part of JacMLDash.
# Distributed under terms of the MIT license.

import json
from jacinle.web.app import route, JacRequestHandler
from .manager import mark_as_stared_by_spec


@route(r'/star/star')
class StarHandler(JacRequestHandler):
    def get(self):
        spec = json.loads(self.get_argument('spec'))
        record = mark_as_stared_by_spec(spec)


@route(r'/star/unstar')
class UnstarHandler(JacRequestHandler):
    def get(self):
        spec = json.loads(self.get_argument('spec'))
        record = mark_as_stared_by_spec(spec, False)

