# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test for text search in page'

    def run(self):
        url = 'https://www.google.com/?hl=EN'
        google_search_image = 'google_search.png'
        search_in_page_image = 'search_in_page.png'

        navigate(url)

        expected_1 = exists(google_search_image, 10)
        assert_true(self, expected_1, 'Wait for google search image to appear')

        open_find()
        type('Gmail')

        expected_2 = exists(search_in_page_image, 10)
        assert_true(self, expected_2, 'Find search in page image')
