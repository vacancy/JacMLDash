#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# File   : main.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 10/23/2018
#
# This file is part of Jacinle.
# Distributed under terms of the MIT license.

import os.path as osp
import jacinle.io as io
from jacinle.logging import get_logger
from jacinle.cli.argument import JacArgumentParser
from jacweb.web import make_app
from mldash.data.orm import init_database, init_project, ProjectMetainfo, Desc, Experiment, Run
from mldash.web.path import get_static_path, get_template_path

import tornado.ioloop

logger = get_logger(__file__)

parser = JacArgumentParser()
parser.add_argument('--logdir', required=True)
parser.add_argument('--port', type=int, default=8081)
args = parser.parse_args()


def main():
    init_database(args.logdir)
    init_project()

    app = make_app([
        'mldash.web.app.index',
        'mldash.web.app.experiment',
        'mldash.web.app.run'
    ], {
        'gzip': True,
        'debug': False,
        'xsrf_cookies': True,

        'static_path': get_static_path(),
        'template_path': get_template_path(),

        "cookie_secret": "20f42d0ae6548e88cf9788e725b298bd",
        "session_secret": "3cdcb1f00803b6e78ab50b466a40b9977db396840c28307f428b25e2277f1bcc",
        "frontend_secret": "asdjikfh98234uf9pidwja09f9adsjp9fd6840c28307f428b25e2277f1bcc",

        "cookie_prefix": 'jac_',
        'session_engine': 'off',
    })
    app.listen(args.port, xheaders=True)

    logger.critical('Mainloop started.')
    loop = tornado.ioloop.IOLoop.current()
    loop.start()


if __name__ == '__main__':
    main()

