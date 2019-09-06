#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# File   : run.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 09/05/2019
#
# This file is part of JacMLDash.
# Distributed under terms of the MIT license.

from jacweb.web import route, JacRequestHandler
from mldash.data.orm import init_database, Desc, Experiment, Run


@route(r'/run')
class RunHandler(JacRequestHandler):
    def get(self):
        desc_name = self.get_argument('desc', '')
        desc = Desc.get_or_none(desc_name=desc_name)
        if desc is None:
            return

        expr_name = self.get_argument('expr', '')
        expr = Experiment.get_or_none(desc=desc, expr_name=expr_name)
        if expr is None:
            return

        run_name  = self.get_argument('run', '')
        run = Run.get_or_none(expr=expr, run_name=run_name)
        if run is None:
            return

        self.render('run.html', run=run, expr=expr, desc=desc)
