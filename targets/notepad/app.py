# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from src.base.target import *


class Target(BaseTarget):
    def __init__(self):
        BaseTarget.__init__(self)
        self.target_name = 'Notepad'

        self.cc_settings = [
            {'name': 'build', 'type': 'list', 'label': 'Build',
             'value': ['build1', 'build2', 'build3'], 'default': 'build1'},
            {'name': 'locale', 'type': 'list', 'label': 'Locale', 'value': ['en-US', 'es-ES'], 'default': 'en-US'},
            {'name': 'highlight', 'type': 'checkbox', 'label': 'Debug using highlighting', 'value': False},
            {'name': 'override', 'type': 'checkbox', 'label': 'Run disabled tests', 'value': False},
            {'name': 'special', 'type': 'checkbox', 'label': 'I am special', 'value': True},
        ]