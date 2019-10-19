#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# File   : client.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 09/06/2019
#
# This file is part of JacMLDash.
# Distributed under terms of the MIT license.

import sys
import contextlib
import jacinle.io as io
from mldash.data.orm import init_database, init_project, Desc, Experiment, Run

__all__ = ['MLDashClient']


class MLDashClient(object):
    def __init__(self, dump_dir):
        self.dump_dir = dump_dir
        init_database(self.dump_dir)
        self.desc = None
        self.expr = None
        self.run = None

    def _refresh(self):
        self.desc = Desc.get_by_id(self.desc.get_id())
        self.expr = Experiment.get_by_id(self.expr.get_id())
        self.run = Run.get_by_id(self.run.get_id())

    def init(self, desc_name, expr_name, run_name, args=None, highlight_args=None, configs=None):
        init_project()
        desc, _ = Desc.get_or_create(desc_name=desc_name)
        expr, _ = Experiment.get_or_create(desc=desc, expr_name=expr_name)
        run = Run(expr=expr, run_name=run_name, command=' '.join(sys.argv))

        run.args = ''
        run.highlight_args = ''

        if args is not None:
            run.args = io.dumps_json(args.__dict__)
            if highlight_args is not None and hasattr(highlight_args, 'highlight_args'):
                run.highlight_args = io.dumps_json(get_highlight_args(args, highlight_args))

        run.configs = ''
        run.highlight_configs = ''

        if configs is not None:
            run.configs = io.dumps_json(configs)
            if getattr(args, 'configs', None) is not None:
                run.highlight_configs = io.dumps_json(args.configs.kvs)

        run.save()

        self.desc = desc
        self.expr = expr
        self.run = run

    @property
    def extra_info_dict(self):
        return self.run.extra_info_dict

    def update(self, **kwargs):
        self._refresh()
        for k, v in kwargs.items():
            if v is not None:
                setattr(self.run, k, v)
        self.run.save()

    def update_parent(self, parent, is_master=False):
        self._refresh()
        self.run.is_master = is_master
        self.run.refer = Run.get_or_none(expr=self.expr, run_name=parent)
        self.run.save()

    @contextlib.contextmanager
    def update_extra_info(self):
        self._refresh()
        yield
        self.run.update_extra_info()
        self.run.save()

    def _log_metric_inner(self, key, value, target, update_func=None):
        if target.metrics is None:
            current = dict()
        else:
            current = io.loads_json(target.metrics)
        if update_func is not None:
            if key in current:
                current[key] = update_func(current[key], value)
            else:
                current[key] = value
        else:
            current[key] = value
        target.metrics = io.dumps_json(current)
        target.save()

    def _log_metric_dist(self, key, value, desc, expr, update_func=None):
        self._refresh()
        if desc: self._log_metric_inner(key, value, self.desc, update_func)
        if expr: self._log_metric_inner(key, value, self.expr, update_func)
        self._log_metric_inner(key, value, self.run, update_func)

    def log_metric(self, key, value, desc=True, expr=True):
        self._log_metric_dist(key, value, desc, expr)

    def log_metric_max(self, key, value, desc=True, expr=True):
        self._log_metric_dist(key, value, desc, expr, max)

    def log_metric_min(self, key, value, desc=True, expr=True):
        self._log_metric_dist(key, value, desc, expr, min)


def get_highlight_args(args, parser):
    highlight_args = parser.highlight_args
    return {k: getattr(args, k) for k in highlight_args if get_default_value_in_parser(parser, k) != getattr(args, k)}


def get_default_value_in_parser(parser, key):
    for rec in parser._option_string_actions.values():
        if rec.dest == key:
            return rec.default
    return None

