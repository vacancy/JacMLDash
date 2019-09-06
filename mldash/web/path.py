#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# File   : template.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 09/05/2019
#
# This file is part of JacMLDash.
# Distributed under terms of the MIT license.

import os.path as osp


def get_template_path():
    return osp.join(osp.dirname(__file__), '_templates')


def get_static_path():
    return osp.join(osp.dirname(__file__), '_static')

