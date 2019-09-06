#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# File   : experiment.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 09/05/2019
#
# This file is part of JacMLDash.
# Distributed under terms of the MIT license.

from jacweb.web import route, JacRequestHandler
from mldash.data.orm import init_database, Desc, Experiment

@route(r'/expr')
class ExprHandler(JacRequestHandler):
    def get(self):
        desc_name = self.get_argument('desc', '')
        desc = Desc.get_or_none(desc_name=desc_name)
        if desc is None:
            return

        expr_name = self.get_argument('expr', '')
        expr = Experiment.get_or_none(desc=desc, expr_name=expr_name)
        if expr is None:
            return

        self.render('experiment.html', expr=expr, desc=desc)
