#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# File   : handler.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 09/06/2019
#
# This file is part of JacMLDash.
# Distributed under terms of the MIT license.

import json
import jacinle.io as io
from jacweb.web import route, JacRequestHandler
from .manager import tensorboard_manager


@route(r'/tensorboard')
class DescHandler(JacRequestHandler):
    def get(self):
        spec = json.loads(self.get_argument('spec', ''))
        record = tensorboard_manager.start(spec['desc'], spec['expr'], spec['runs'])
        host = self.request.host
        if ':' in host:
            host = host[:host.find(':')]
        self.write(io.dumps_json({'url': 'http://' + host + ':' + str(record['port'])}))

