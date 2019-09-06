#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# File   : ui_methods.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 09/06/2019
#
# This file is part of JacMLDash.
# Distributed under terms of the MIT license.

import json
from jacinle.utils.printing import kvformat
from .config import allow_custom_ui_method


@allow_custom_ui_method
def format_kv(handler, kvs):
    if kvs is None or kvs == '':
        return '<pre></pre>'
    if not isinstance(kvs, dict):
        kvs = json.loads(kvs)
    return '<pre>' + kvformat(kvs) + '</pre>'


@allow_custom_ui_method
def format_kv_inline(handler, kvs):
    if kvs is None or kvs == '':
        return ''
    if not isinstance(kvs, dict):
        kvs = json.loads(kvs)
    kvs = {k: kvs[k] for k in sorted(kvs.keys())}
    return '<code>' + '; '.join(['{}={}'.format(k, '{:.4f}'.format(v) if isinstance(v, (int, float)) else v) for k, v in kvs.items()]) + '</code>'


@allow_custom_ui_method
def format_fpath(handler, path):
    return '<code>' + path + '</code>'


@allow_custom_ui_method
def format_log_fpath(handler, path):
    return '<code>' + path + '</code>'


@allow_custom_ui_method
def format_tb_link(handler, port):
    host = handler.request.host
    if ':' in host:
        host = host[:host.find(':')]
    link = 'http://' + host + ':' + str(port)
    return '<a href="{link}" target="_blank">{link}</a>'.format(link=link)

