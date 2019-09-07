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
from mldash.data.orm import init_database, Desc, Experiment, Run
from mldash.plugins.tensorboard.manager import tensorboard_manager


@route(r'/desc')
class DescHandler(JacRequestHandler):
    def get(self):
        desc_name = self.get_argument('desc', '')
        desc = Desc.get_or_none(desc_name=desc_name)
        if desc is None:
            return

        self.render('desc.html', desc=desc)


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

        self.render('experiment.html', expr=expr, desc=desc, tensorboards=tensorboard_manager.get_running_tensorboards(desc_name, expr_name))


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


@route(r'.*/update/text')
class UpdateTextHandler(JacRequestHandler):
    def get(self):
        def get():
            desc_name = self.get_argument('desc', '')
            desc = Desc.get_or_none(desc_name=desc_name)
            if desc is None:
                return None

            expr_name = self.get_argument('expr', '')
            expr = Experiment.get_or_none(desc=desc, expr_name=expr_name)
            if expr is None:
                return desc

            run_name  = self.get_argument('run', '')
            run = Run.get_or_none(expr=expr, run_name=run_name)
            if run is None:
                return expr

            return run

        record = get()
        setattr(record, self.get_argument('key'), self.get_argument('value'))
        record.save()

