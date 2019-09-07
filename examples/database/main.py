#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# File   : main.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 09/05/2019
#
# This file is part of JacMLDash.
# Distributed under terms of the MIT license.

import time
from mldash.data.orm import init_database, ProjectMetainfo, Desc, Experiment, Run


def main():
    init_database('.')

    ProjectMetainfo.set_all({
        'title': 'Test',
        'create_time': '2019-09-05 15:44:27',
        'update_time': '2019-09-05 15:44:27'
    })

    print(ProjectMetainfo.get_all())

    print('Create the desc')
    desc, _ = Desc.get_or_create(desc_name='desc_xxx')
    print('Create the expr')
    expr, _ = Experiment.get_or_create(expr_name='expr1', desc=desc)

    print('Create the runs')
    train_run = Run(expr=expr, run_name='train1' + str(time.time()), command='jac-run xxx', args='{xxx}', configs='{xxx}', highlight_args='{yyy}', highlight_configs='{yyy}')
    test_run = Run(expr=expr, run_name='test1'+  str(time.time()), command='jac-run xxx', args='{xxx}', configs='{xxx}', highlight_args='{yyy}', highlight_configs='{yyy}', refer=train_run)

    from IPython import embed;  embed()

    train_run.save()
    test_run.save()


if __name__ == '__main__':
    main()

