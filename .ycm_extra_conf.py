#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# File   : .ycm_extra_conf.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 02/16/2019
#
# This file is part of NSCL-PyTorch.
# Distributed under terms of the MIT license.

import os.path as osp


def PythonSysPath(**kwargs):
    sys_path = kwargs['sys_path']
    sys_path.insert(0, osp.dirname(__file__))

    return sys_path
