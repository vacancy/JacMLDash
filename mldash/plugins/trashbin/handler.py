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
import jacinle.io as io
from jacweb.web import route, JacRequestHandler
from .manager import mark_as_trash_by_spec


@route(r'/trashbin/delete')
class TrashbinDeleteHandler(JacRequestHandler):
    def get(self):
        spec = json.loads(self.get_argument('spec'))
        record = mark_as_trash_by_spec(spec)

