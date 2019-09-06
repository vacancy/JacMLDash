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
import socket, errno
import atexit

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
        self.running_tensorboards = collections.defaultdict(list)
        self.index = 0
        atexit.register(self._kill_all)

    def start(self, desc_name, expr_name, runs):
        desc = Desc.get_or_none(desc_name=desc_name)
        if desc is None:
            return None
        expr = Experiment.get_or_none(desc=desc, expr_name=expr_name)
        if expr is None:
            return None

        logdirs = dict()
        for run_name in runs:
            run = Run.get_or_none(expr=expr, run_name=run_name)
            if run is None:
                continue
            key = run.run_name
            value = run.tb_dir
            if value is not None and value != '':
                logdirs[key] = value

        if len(logdirs) == 0:
            return None

        logdirs_string = ','.join(['{}:{}'.format(k, v) for k, v in logdirs.items()])
        port = find_port()

        process = subprocess.Popen(
            ['tensorboard', '--logdir', logdirs_string, '--port', str(port)],
            stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w')
        )
        record = dict(index=self.index, logdirs=logdirs, logdirs_string=logdirs_string, port=port, process=process)

        self.index += 1
        self.running_tensorboards[desc_name, expr_name].append(record)
        return record

    def terminate(self, desc_name, expr_name, index):
        found = None
        for x in self.running_tensorboards[desc_name, expr_name]:
            if x['index'] == index:
                found = x
                break
        if found is not None:
            found.terminate()
            self.running_tensorboards[desc_name, expr_name].remove(found)

    def get_running_tensorboards(self, desc_name, expr_name):
        self._clean_up_running_tensorboards(desc_name, expr_name)
        return self.running_tensorboards[desc_name, expr_name]

    def _clean_up_running_tensorboards(self, desc_name, expr_name):
        self.running_tensorboards[desc_name, expr_name] = [x for x in self.running_tensorboards[desc_name, expr_name] if x['process'].poll() is None]

    def _kill_all(self):
        for values in self.running_tensorboards.values():
            for v in values:
                v['process'].terminate()


tensorboard_manager = TensorboardManager()

