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
from jacinle.utils.imp import load_source
from jacweb.web import make_app
from mldash.data.orm import init_database, init_project, ProjectMetainfo, Desc, Experiment, Run
from mldash.web.path import get_static_path, get_template_path
from mldash.web.ui_methods import get_ui_methods, register_ui_methods
from mldash.web.run_methods import register_run_methods
from mldash.web.custom_pages import register_custom_pages

import tornado.ioloop

logger = get_logger(__file__)

parser = JacArgumentParser()
parser.add_argument('--logdir', required=True)
parser.add_argument('--port', type=int, default=8081)
parser.add_argument('--debug', action='store_true')
parser.add_argument('--cli', action='store_true')
args = parser.parse_args()


def main():
    init_database(args.logdir)
    init_project()

    py_filename = osp.join('jacmldash.py')
    if osp.isfile(py_filename):
        logger.critical('Loading JacMLDash config: {}.'.format(osp.abspath(py_filename)))
        config = load_source(py_filename)
        if hasattr(config, 'ui_methods'):
            register_ui_methods(config.ui_methods)
        if hasattr(config, 'run_methods'):
            register_run_methods(config.run_methods)
        if hasattr(config, 'custom_pages'):
            register_custom_pages(config.custom_pages)

    if args.cli:
        from IPython import embed; embed()
        return

    app = make_app([
        'mldash.web.app.index',
        'mldash.web.app.experiment',
        'mldash.plugins.tensorboard.handler',
        'mldash.plugins.trashbin.handler',
        'mldash.plugins.star.handler'
    ], {
        'gzip': True,
        'debug': args.debug,
        'xsrf_cookies': True,

        'static_path': get_static_path(),
        'template_path': get_template_path(),
        'ui_methods': get_ui_methods(),

        "cookie_secret": "20f42d0ae6548e88cf9788e725b298bd",
        "session_secret": "3cdcb1f00803b6e78ab50b466a40b9977db396840c28307f428b25e2277f1bcc",
        "frontend_secret": "asdjikfh98234uf9pidwja09f9adsjp9fd6840c28307f428b25e2277f1bcc",

        "cookie_prefix": 'jac_',
        'session_engine': 'off',
    })
    app.listen(args.port, xheaders=True)

    logger.critical('Mainloop started. Port: {}.'.format(args.port))
    loop = tornado.ioloop.IOLoop.current()
    loop.start()


if __name__ == '__main__':
    main()

