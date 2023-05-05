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
import peewee
import time
import random
import jacinle
import jacinle.io as io
from mldash.orm import init_database, Desc, Experiment, Run

__all__ = ['MLDashClient']

logger = jacinle.get_logger(__file__)


class MLDashClient(object):
    def __init__(self, dump_dir):
        self.dump_dir = dump_dir
        init_database(self.dump_dir)
        self.desc = None
        self.expr = None
        self.run = None

    def _refresh(self):
        self.desc = load_retry(Desc, self.desc)
        self.expr = load_retry(Experiment, self.expr)
        self.run = load_retry(Run, self.run)

    def init(self, desc_name, expr_name, run_name, args=None, highlight_args=None, configs=None):
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
            highlight_configs = get_highlight_configs(args)
            if highlight_configs is not None:
                run.highlight_configs = io.dumps_json(highlight_configs)

        save_retry(run)

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
        save_retry(self.run)

    def update_parent(self, parent, is_master=False):
        self._refresh()
        self.run.is_master = is_master
        self.run.refer = Run.get_or_none(expr=self.expr, run_name=parent)
        save_retry(self.run)

    @contextlib.contextmanager
    def update_extra_info(self):
        self._refresh()
        yield
        self.run.update_extra_info()
        save_retry(self.run)

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
        save_retry(target)

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


def load_retry(cls, default, max_retries=5, wait=(10, 200)):
    last_exc = None
    for i in range(max_retries):
        try:
            return cls.get_by_id(default.get_id())
        except peewee.OperationalError as e:
            time.sleep(1 / 1000 * random.randint(wait[0], wait[1]))
            last_exc = e
    logger.warning('Database refresh failed after {} trials. Last exception message is {}.'.format(max_retries, last_exc))
    return default


def save_retry(model, max_retries=5, wait=(10, 200)):
    flag = False
    last_exc = None
    for i in range(max_retries):
        try:
            model.save()
            flag = True
            break
        except peewee.OperationalError as e:
            time.sleep(1 / 1000 * random.randint(wait[0], wait[1]))
            last_exc = e
    if not flag:
        logger.warning('Database update failed after {} trials. Last exception message is {}.'.format(max_retries, last_exc))


def get_highlight_configs_raw(args):
    if hasattr(args, 'configs'):
        return args.configs
    elif hasattr(args, 'config'):
        return args.config
    else:
        return None


def get_highlight_configs(args):
    configs = get_highlight_configs_raw(args)
    if configs is None:
        return None

    from jacinle.cli.argument import _KV

    data = dict()
    if isinstance(configs, (tuple, list)):
        for configs_kv in configs:
            if isinstance(configs_kv, _KV):
                for k, v in configs_kv.kvs:
                    data[k] = v
    elif isinstance(configs, _KV):
        for k, v in configs.kvs:
            data[k] = v

    return data

