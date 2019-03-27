# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This is a test for text search in page'
        self.enabled = False

    def run(self):
        google_search_pattern = Pattern('google_search.png')
        search_in_page_pattern = Pattern('search_in_page_image.png')

        navigate('https://www.google.com/?hl=EN')

        expected_1 = exists(google_search_pattern, 10)
        assert_true(self, expected_1, 'Wait for google search image to appear')

        open_find()
        type('Images')

        expected_2 = exists(search_in_page_pattern, 10)
        assert_true(self, expected_2, 'Find search in page image')
