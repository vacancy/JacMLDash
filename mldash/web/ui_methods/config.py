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

__all__ = ['register_ui_methods', 'get_ui_methods']


_custom_ui_methods = None


def register_ui_methods(cls):
    global _custom_ui_methods
    _custom_ui_methods = cls


def get_ui_methods():
    from . import ui_methods
    return ui_methods


def get_custom_ui_method(name):
    if _custom_ui_methods is not None and hasattr(_custom_ui_methods, name):
        return getattr(_custom_ui_methods, name)
    return None


def allow_custom_ui_method(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        custom = get_custom_ui_method(func.__name__)
        if custom is not None:
            return custom(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapped

