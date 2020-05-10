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
from mldash.web.run_methods import get_run_methods
from mldash.web.custom_pages import get_custom_pages


@route(r'/desc')
class DescHandler(JacRequestHandler):
    def get(self):
        desc_name = self.get_argument('desc', '')

        if desc_name == '__all__':
            descs = Desc.select().execute()
            self.render('desc_all.html', descs=descs, tensorboards=tensorboard_manager.get_running_tensorboards(), star_only=False)
            return

        if desc_name == '__star__':
            descs = Desc.select().execute()
            self.render('desc_all.html', descs=descs, tensorboards=tensorboard_manager.get_running_tensorboards(), star_only=True)
            return

        desc = Desc.get_or_none(desc_name=desc_name)
        if desc is None:
            return

        self.render('desc.html', desc=desc, tensorboards=tensorboard_manager.get_running_tensorboards(desc_name))


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

        self.render('run.html', run=run, expr=expr, desc=desc, run_methods=get_run_methods())


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


@route(r'/runcmd')
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

        run_methods = get_run_methods()
        cmd_name = self.get_argument('cmd', '')
        method = None
        for m in run_methods:
            if m.__name__ == cmd_name:
                method = m

        if method is None:
            return

        import multiprocessing
        import sys
        self.write('<pre>')
        self.flush()
        sys.stdout = self
        sys.stderr = self
        proc = multiprocessing.Process(target=method, args=(run, ))
        proc.start()
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        proc.join()
        self.write('</pre>')
        self.flush()
        self.finish()


@route(r'/custom')
class CustomPageHandler(JacRequestHandler):
    def get(self):
        custom_pages = get_custom_pages()
        page_name = self.get_argument('page', '')

        page = None
        for p in custom_pages:
            if p.__name__ == 'handle_' + page_name:
                page = p

        if page is None:
            return

        page(self)

