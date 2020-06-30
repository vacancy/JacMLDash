#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# File   : demo.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 06/24/2020
#
# This file is part of JacMLDash.
# Distributed under terms of the MIT license.

import argparse
import time
from mldash.client import MLDashClient

mldash = MLDashClient('./dumps')

parser = argparse.ArgumentParser()
parser.add_argument('--epochs', type=int, default=100, metavar='N', help='number of total epochs to run')
parser.add_argument('--batch-size', type=int, default=32, metavar='N', help='batch size')
parser.add_argument('--lr', type=float, default=0.001, metavar='N', help='initial learning rate')
parser.highlight_args = ['batch_size', 'lr']  # denote a list of names that you want to highlight.
args = parser.parse_args()

configs = dict(
)  # optional. A json-seriealizable object.


def main():
    run_name = 'trainval-{}'.format(time.strftime('%Y-%m-%d-%H-%M-%S'))
    mldash.init(desc_name='desc_demo', expr_name='default', run_name=run_name, args=args, highlight_args=parser, configs=configs)

    # after initialization, you can update values.
    # below are four built-in values, including: metainfo file, log file, meter file, tensorboard directory.
    # mldash.update(metainfo_file=args.meta_file, log_file=args.log_file, meter_file=args.meter_file, tb_dir=args.tb_dir)

    for epoch in range(1, 10 + 1):
        meters = {
            'loss': 0.1,
            'validation/loss': 0.1,
            'acc': 0.9,
            'validation/acc': 0.9
        }  # generate a fake log values.

        mldash.log_metric('epoch', epoch, desc=False, expr=False)
        for key, value in meters.items():
            if key.startswith('loss') or key.startswith('validation/loss'):
                mldash.log_metric_min(key, value)
        for key, value in meters.items():
            if key.startswith('acc') or key.startswith('validation/acc'):
                mldash.log_metric_max(key, value)

        with mldash.update_extra_info():
            # extra_info_dict is a dict. This interface allows you to log anything you want.
            mldash.extra_info_dict.setdefault('Epochs', []).append(f'Epoch {epoch:3}')


if __name__ == '__main__':
    main()

