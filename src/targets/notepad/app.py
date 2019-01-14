# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from src.base.target import *


class Target(BaseTarget):
    def __init__(self):
        BaseTarget.__init__(self)
        self.target_name = 'Notepad'
