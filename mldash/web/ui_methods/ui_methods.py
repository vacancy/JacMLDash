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
from jacinle.utils.printing import kvformat, stformat
from jacinle.utils.meta import dict_deep_kv
from .config import allow_custom_ui_method


@allow_custom_ui_method
def format_kv(handler, kvs):
    if kvs is None or kvs == '':
        return '<pre>N/A</pre>'
    if not isinstance(kvs, dict):
        kvs = json.loads(kvs)
    return '<pre>' + kvformat(kvs) + '</pre>'


@allow_custom_ui_method
def format_kv_recursive_flat(handler, kvs):
    if kvs is None or kvs == '':
        return '<pre>N/A</pre>'
    if not isinstance(kvs, dict):
        kvs = json.loads(kvs)
    return '<pre>' + kvformat({k: v for k, v in dict_deep_kv(kvs) if not '__' in k}) + '</pre>'


@allow_custom_ui_method
def format_kv_recursive(handler, kvs):
    if kvs is None or kvs == '':
        return '<pre>N/A</pre>'
    if not isinstance(kvs, dict):
        kvs = json.loads(kvs)
    return '<div class="inline-pre">' + stformat(kvs, indent_format='&nbsp;&nbsp;', end_format='<br />') + '</div>'


@allow_custom_ui_method
def format_kv_inline(handler, kvs, html=True):
    if kvs is None or kvs == '':
        if html:
            return '<code>N/A</code>'
        else:
            return ''
    if not isinstance(kvs, dict):
        kvs = json.loads(kvs)
    kvs = {k: kvs[k] for k in sorted(kvs.keys())}
    ret = '; '.join(['{}={}'.format(k, '{:.6f}'.format(v) if isinstance(v, (float)) else v) for k, v in kvs.items()])
    if html:
        return '<code>' + ret + '</code>'
    return ret


def format_kv_inline_tb(handler, kvs):
    if kvs is None or kvs == '':
        return ''
    if not isinstance(kvs, dict):
        kvs = json.loads(kvs)
    kvs = {k: kvs[k] for k in sorted(kvs.keys())}
    ret = '_'.join(['{} = {}'.format(k, '{:.6f}'.format(v) if isinstance(v, (float)) else v) for k, v in kvs.items()])
    return ret


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


@allow_custom_ui_method
def format_extra_items(handler, run):
    return dict()


@allow_custom_ui_method
def format_extra_summary_items(handler, run):
    return dict()


def is_deleted(handler, run):
    from mldash.plugins.trashbin import is_trash
    return is_trash(run)


def is_stared(handler, run):
    from mldash.plugins.star import is_stared
    return is_stared(run)

