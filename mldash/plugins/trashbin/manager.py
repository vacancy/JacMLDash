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


def mark_as_trash(run):
    run.extra_info_dict['is_deleted'] = True
    run.update_extra_info()


def is_trash(run):
    return run.extra_info_dict.get('is_deleted', False)


def mark_as_trash_by_spec(specs):
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

        mark_as_trash(run)
        run.save()

