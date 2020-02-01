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

__all__ = ['register_custom_pages', 'get_custom_pages']


_custom_custom_pages = []


def register_custom_pages(cls):
    global _custom_custom_pages
    _custom_custom_pages = list(_find_custom_custom_pages(cls))


def get_custom_pages():
    return _custom_custom_pages


def _find_custom_custom_pages(cls):
    for method in dir(cls):
        if method.startswith('handle_'):
            yield getattr(cls, method)
