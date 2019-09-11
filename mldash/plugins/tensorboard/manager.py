#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# File   : manager.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 09/06/2019
#
# This file is part of JacMLDash.
# Distributed under terms of the MIT license.

import os
import subprocess
import collections
import socket
import errno
import atexit
import threading

from mldash.data.orm import Desc, Experiment, Run

__all__ = ['tensorboard_manager']


def _check_port_usage(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", port))
    except socket.error as e:
        if e.errno == errno.EADDRINUSE:
            return False
        return False
    s.close()
    return True


def find_port(start=6006, max_tries=40):
    for x in range(start, start + max_tries):
        if _check_port_usage(x):
            return x
    return None


class TensorboardManager(object):
    def __init__(self):
        self.running_tensorboards = list()
        self.mutex = threading.Lock()
        self.index = 0
        atexit.register(self._kill_all)

    def start(self, specs):
        logdirs = dict()
        exprs = set()
        descs = set()
        for spec in specs:
            desc = Desc.get_or_none(desc_name=spec['desc'])
            if desc is None:
                continue
            expr = Experiment.get_or_none(desc=desc, expr_name=spec['expr'])
            if expr is None:
                continue
            run = Run.get_or_none(expr=expr, run_name=spec['run'])
            if run is None:
                continue

            key = run.expr.desc.desc_name + '/' + run.expr.expr_name + '/' + run.run_name + '/' + spec['highlight']
            key = key.replace(';', '_').replace(' ', '')
            value = run.tb_dir
            if value is not None and value != '':
                logdirs[key] = value
            descs.add(spec['desc'])
            exprs.add((spec['desc'], spec['expr']))

        if len(logdirs) == 0:
            return None

        logdirs_string = ','.join(['{}:{}'.format(k, v) for k, v in logdirs.items()])
        port = find_port()

        process = subprocess.Popen(
            ['tensorboard', '--logdir', logdirs_string, '--port', str(port)],
            stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w')
        )
        record = dict(index=self.index, logdirs=logdirs, logdirs_string=logdirs_string, descs=descs, exprs=exprs, port=port, process=process)

        self.index += 1
        with self.mutex:
            self.running_tensorboards.append(record)
        return record

    def terminate(self, index):
        with self.mutex:
            found = None
            for x in self.running_tensorboards:
                if x['index'] == index:
                    found = x
                    break
            if found is not None:
                found['process'].terminate()
                self.running_tensorboards.remove(found)

    def get_running_tensorboards(self, desc_name=None, expr_name=None):
        with self.mutex:
            self._clean_up_running_tensorboards()
            if desc_name is None:
                return self.running_tensorboards
            if expr_name is None:
                return [x for x in self.running_tensorboards if desc_name in x['descs']]
            return [x for x in self.running_tensorboards if (desc_name, expr_name) in x['exprs']]

    def _clean_up_running_tensorboards(self):
        self.running_tensorboards = [x for x in self.running_tensorboards if x['process'].poll() is None]

    def _kill_all(self):
        for v in self.running_tensorboards:
            v['process'].terminate()


tensorboard_manager = TensorboardManager()

