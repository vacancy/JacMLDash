#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# File   : config.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 09/06/2019
#
# This file is part of JacMLDash.
# Distributed under terms of the MIT license.

import functools

__all__ = ['register_run_methods', 'get_run_methods']


_custom_run_methods = []


def register_run_methods(cls):
    global _custom_run_methods
    _custom_run_methods = list(_find_custom_run_methods(cls))


def get_run_methods():
    return _custom_run_methods


def _find_custom_run_methods(cls):
    for method in dir(cls):
        if method.startswith('run_'):
            yield getattr(cls, method)
