
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Firefox can be set to display the home page on launch'
        self.test_case_id = '143543'
        self.test_suite_id = '2241'
        self.locales = ['en-US']

    def run(self):
        navigate('about:preferences#home')
