# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from argparse import Namespace
import argparse
import logging
import os

from src.core.api.os_helpers import OSHelper

logger = logging.getLogger(__name__)
iris_args = None


def get_core_args():
    global iris_args
    home = os.path.expanduser('~')

    log_level_strings = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']

    def log_level_string_to_int(log_level_string):
        if log_level_string not in log_level_strings:
            logger.error('Invalid choice: %s (choose from %s)', log_level_string, log_level_strings)
            exit(1)

        log_level_int = getattr(logging, log_level_string, logging.INFO)
        assert isinstance(log_level_int, int)
        return log_level_int

    parser = argparse.ArgumentParser(description='Iris core arguments', prog='iris')
    target_dir = os.path.join(os.path.realpath(os.path.split(__file__)[0] + '/../../..'), 'targets')
    target_list = [f.path for f in os.scandir(target_dir) if f.is_dir()]
    for idx, target in enumerate(target_list):
        target_list[idx] = os.path.basename(os.path.normpath(target))

    parser.add_argument('target', nargs='?', action='store', type=str, help='Target name', choices=target_list)

    parser.add_argument('-a', '--rerun',
                        help='Rerun last failed tests',
                        action='store_true')
    parser.add_argument('-b', '--highlight',
                        help='Highlight patterns and click actions',
                        action='store_true')
    parser.add_argument('-c', '--clear',
                        help='Clear run data',
                        default=False,
                        action='store_true')
    parser.add_argument('-e', '--email',
                        help='Submit email report',
                        action='store_true')
    parser.add_argument('-i', '--level',
                        help='Set the logging output level',
                        type=log_level_string_to_int,
                        dest='level',
                        default='INFO')
    parser.add_argument('-k', '--control',
                        help='Display control center',
                        action='store_true')
    parser.add_argument('-l', '--locale',
                        help='Locale to use for pattern search',
                        action='store',
                        default='en-US')
    parser.add_argument('-m', '--mouse',
                        help='Change mouse speed',
                        type=float,
                        action='store',
                        default=0.5)
    parser.add_argument('-n', '--no_check',
                        help='Skip key lock check on startup',
                        action='store_true')
    parser.add_argument('-o', '--override',
                        help='Override disabled tests',
                        action='store_true')
    parser.add_argument('-p', '--port',
                        help='Port to use for local web server',
                        type=int,
                        action='store',
                        default=2000)
    parser.add_argument('-t', '--test',
                        help='Partial or full test names or paths to execute',
                        action='store',
                        default='')
    parser.add_argument('-w', '--workdir',
                        help='Path to working directory',
                        type=os.path.abspath,
                        action='store',
                        default='%s/.iris' % home)
    parser.add_argument('-x', '--exclude',
                        help='Partial or full test names or paths to exclude',
                        action='store',
                        default='')
    parser.add_argument('-z', '--resize',
                        help='Convert hi-res images to normal',
                        action='store_true')
    parser.add_argument('-vk', '--virtual_keyboard',
                        help='Use the virtual/fake keyboard for virtual environments',
                        action='store_true',
                        default=False)

    global iris_args
    if iris_args is None:
        iris_args = parser.parse_known_args()[0]

    if iris_args.virtual_keyboard and not OSHelper.is_linux():
        logger.error("Virtual keyboard is available only on LINUX.")
        exit(1)

    return iris_args


def set_core_arg(arg, value):
    logger.debug('Set core arg %s = %s' % (arg, value))
    global iris_args
    arg_dict = vars(iris_args)
    arg_dict[arg] = value
    iris_args = Namespace(**arg_dict)
