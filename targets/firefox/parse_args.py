# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import argparse
import logging

logger = logging.getLogger(__name__)


def get_target_args():
    parser = argparse.ArgumentParser(description='Firefox specific arguments', prog='iris')
    parser.add_argument('-f', '--firefox',
                        help='Firefox version to test',
                        action='store',
                        default='latest-beta')
    parser.add_argument('-l', '--locale',
                        help='Locale to use for Firefox',
                        action='store',
                        default='en-US')
    parser.add_argument('-u', '--update_channel',
                        help='Update channel profile preference',
                        action='store')

    return parser.parse_known_args()[0]
