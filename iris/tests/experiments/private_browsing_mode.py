# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This is a test for checking private browsing navigation'
        self.enabled = False

    def run(self):
        private_browsing_pattern = Pattern('private_browsing.png')
        google_search_pattern = Pattern('google_search.png')

        new_private_window()

        expected_1 = exists(private_browsing_pattern, 10)
        assert_true(self, expected_1, 'Find private browsing image')

        navigate('https://www.google.com/?hl=EN')

        expected_2 = exists(google_search_pattern, 10)
        assert_true(self, expected_2, 'Find google search image')
