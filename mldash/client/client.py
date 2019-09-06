#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# File   : client.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 09/06/2019
#
# This file is part of JacMLDash.
# Distributed under terms of the MIT license.

from mldash.data.orm import init_database, init_project, Desc, Experiment, Run
import jacinle.io as io

__all__ = ['MLDashClient']


class MLDashClient(object):
    def ___init__(self, dump_dir):
        self.dump_dir = dump_dir
        init_database(self.dump_dir)
        self.desc = None
        self.expr = None
        self.run = None

    def init(self, desc_name, expr_name, run_name, args=None, highlight_args=None, configs=None):
        init_project()
        desc = Desc.get_or_create(desc_name=desc_name)
        expr = Experiment.get_or_create(desc=desc, expr_name=expr_name)
        run = Run(expr=expr, run_name=run_name, command=' '.join(sys.argv))

        if args is not None:
            run.args = io.dumps_json(args.__dict__, compressed=False)
            if highlight_args is not None:
                run.highlight_args = io.dumps_json(get_highlight_args(args, highlight_args), compressed=False)

        if configs is not None:
            run.configs = io.dumps_json(configs, compressed=False)
            if getattr(args, 'configs', None) is not None:
                run.highlight_configs = io.dumps_json(args.configs.kvs, compressed=False)

        run.save()

        self.desc = desc
        self.expr = expr
        self.run = run

    def update(self, **kwargs):
        for k, v in kwargs.items():
            if v is not None:
                setattr(self.run, k, v)
        self.run.save()


def get_highlight_args(args, highlight_args):
    return {k: getattr(args, k) for k in highlight_args}

