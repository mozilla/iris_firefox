# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import argparse
import logging

logger = logging.getLogger(__name__)


def get_target_args():
    parser = argparse.ArgumentParser(description='Notepad specific arguments', prog='iris')
    parser.add_argument('-n1', '--notepad_first_argument',
                        help='Notepad first argument',
                        action='store',
                        default='notepad first argument')
    parser.add_argument('-n2', '--notepad_second_argument',
                        help='Notepad second argument',
                        action='store',
                        default='notepad second argument')
    parser.add_argument('-n3', '--notepad_third_argument',
                        help='Notepad third argument',
                        action='store',
                        default='notepad third argument')

    return parser.parse_known_args()[0]
