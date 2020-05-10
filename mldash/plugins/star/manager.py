#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# File   : manager.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 09/08/2019
#
# This file is part of JacMLDash.
# Distributed under terms of the MIT license.

from mldash.data.orm import Desc, Experiment, Run


def mark_as_stared(run, value=True):
    run.extra_info_dict['is_stared'] = value
    run.update_extra_info()


def is_stared(run):
    return run.extra_info_dict.get('is_stared', False)


def mark_as_stared_by_spec(specs, value=True):
    for spec in specs:
        desc = Desc.get_or_none(desc_name=spec['desc'])
        if desc is None:
            continue
        expr = Experiment.get_or_none(desc=desc, expr_name=spec['expr'])
        if expr is None:
            continue
        run = Run.get_or_none(expr=expr, run_name=spec['run'])
        if run is None:
            continue

        mark_as_stared(run, value)
        run.save()

