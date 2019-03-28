# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This is a test of basic URL navigation via awesomebar.'
        self.enabled = False

    def run(self):
        navigate('https://www.google.com/?hl=EN')
        google_search_pattern = Pattern('google_search.png')
        expected_1 = exists(google_search_pattern, 10)
        assert_true(self, expected_1, 'Find image')
