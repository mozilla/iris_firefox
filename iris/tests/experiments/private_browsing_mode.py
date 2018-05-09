# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test for checking private browsing navigation'

    def run(self):
        url = 'https://www.google.com/?hl=EN'
        private_browsing_image = 'private_browsing.png'
        google_search_image = 'google_search.png'

        # check if incognito mode works
        new_private_window()

        expected_1 = exists(private_browsing_image, 10)
        assert_true(self, expected_1, 'Find private browsing image')

        # check basic_url in incognito mode
        navigate(url)

        expected_2 = exists(google_search_image, 10)
        assert_true(self, expected_2, 'Find google search image')
