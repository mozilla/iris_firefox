# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.test_case_id = '105525'
        self.test_suite_id = '1956'
        self.meta = 'Firefox can be set to no longer accept cookies from visited websites.'
        self.locale = ['en-US']

    def run(self):
        pass
