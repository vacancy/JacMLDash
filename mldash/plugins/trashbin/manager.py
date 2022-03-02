#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# File   : manager.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 09/08/2019
#
# This file is part of JacMLDash.
# Distributed under terms of the MIT license.

from mldash.orm import Desc, Experiment, Run


def mark_as_trash(run):
    run.extra_info_dict['is_deleted'] = True
    run.update_extra_info()
    run.save()


def is_trash(run):
    return run.extra_info_dict.get('is_deleted', False)


def mark_as_trash_by_spec(specs):
    failed = list()
    for spec in specs:
        try:
            name = spec['desc']
            x = Desc.get_or_none(desc_name=spec['desc'])
            if x is None:
                raise CannotDeleteException(name)

            if 'expr' in spec:
                name += '/' + spec['expr']
                x = Experiment.get_or_none(desc=x, expr_name=spec['expr'])
                if x is None:
                    raise CannotDeleteException(name)
            else:
                check_empty_record(x, 'exprs', name)

            if 'run' in spec:
                name += '/' + spec['run']
                x = Run.get_or_none(expr=x, run_name=spec['run'])
                if x is None:
                    raise CannotDeleteException(name)
            else:
                check_empty_record(x, 'runs', name)

            mark_as_trash(x)
        except CannotDeleteException as e:
            failed.append(str(e))
    return failed


class CannotDeleteException(Exception):
    pass


def check_empty_record(model, key, name):
    flag = True
    for x in getattr(model, key):
        if not is_trash(x):
            flag = False
    return flag

