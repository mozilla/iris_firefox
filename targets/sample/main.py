# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from src.base.target import *


class Target(BaseTarget):
    def __init__(self):
        BaseTarget.__init__(self)
        self.args = self.get_target_args()
        self.target_name = 'Sample'

        self.cc_settings = [
            {'name': 'build', 'type': 'list', 'label': 'Build',
             'value': ['build1', 'build2', 'build3'], 'default': 'build1'},
            {'name': 'locale', 'type': 'list', 'label': 'Locale', 'value': ['en-US', 'es-ES'], 'default': 'en-US'},
            {'name': 'highlight', 'type': 'checkbox', 'label': 'Debug using highlighting'},
            {'name': 'override', 'type': 'checkbox', 'label': 'Run disabled tests'},
            {'name': 'special', 'type': 'checkbox', 'label': 'I am special'},
        ]

    def get_target_args(self):
        parser = argparse.ArgumentParser(description='Sample-specific arguments', prog='iris')
        parser.add_argument('-u', '--sample_first_argument',
                            help='Sample first argument',
                            action='store',
                            default='sample first argument')
        parser.add_argument('-v', '--sample_second_argument',
                            help='Sample second argument',
                            action='store',
                            default='sample second argument')
        parser.add_argument('-y', '--sample_third_argument',
                            help='Sample third argument',
                            action='store',
                            default='sample third argument')

        return parser.parse_known_args()[0]