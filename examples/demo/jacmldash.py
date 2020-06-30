#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# File   : jacmldash.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 06/30/2020
#
# This file is part of JacMLDash.
# Distributed under terms of the MIT license.

# jacmldash.py is a config file that will be processed when you initialize the jacmldash web interface.
# It contains a set of hooks that will be executed by the web interface to render the web pages.

import os.path as osp
import json


class UIMethods(object):
    # format_extra_items is a useful function that returns a dict mapping from section titles to (html) texts.
    def format_extra_items(self, handler, run):
        last_epoch = run.extra_info_dict['Epochs'][-1]
        return {
            'Last Epoch': last_epoch
        }


ui_methods = UIMethods()
