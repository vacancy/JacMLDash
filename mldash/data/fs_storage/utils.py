#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# File   : utils.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 05/25/2019
#
# This file is part of JacMLDash.
# Distributed under terms of the MIT license.

import os
import jacinle.io as io
from jacinle.logging import get_logger
from jacinle.utils.filelock import FileLock

logger = get_logger(__file__)


def safe_dump(fname, data):
    temp_fname = 'temp.' + fname
    lock_fname = 'lock.' + fname

    with FileLock(lock_fname, 10) as flock:
        if flock.is_locked:
            io.dump(temp_fname, data)
            os.replace(temp_fname, fname)
            return True
        else:
            logger.warning('Cannot lock the file: {}.'.format(fname))
            return False

