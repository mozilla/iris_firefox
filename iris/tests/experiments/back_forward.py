# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test of browser back/forward'

    def run(self):
        url = 'about:home'
        search_the_web_image = 'search_the_web.png'
        google_search_image = 'google_search.png'
        back_pattern = NavBar.BACK_BUTTON
        forward_pattern = NavBar.FORWARD_BUTTON

        navigate(url)

        expected_1 = exists(search_the_web_image, 10)
        assert_true(self, expected_1, 'Find search the web image')

        navigate('https://www.google.com/?hl=EN')

        expected_2 = exists(google_search_image, 10)
        assert_true(self, expected_2, 'Find google search image')

        wait(back_pattern)
        click(back_pattern)

        assert_true(self, expected_1, 'Find search the web image')

        wait(forward_pattern)
        click(forward_pattern)
        assert_true(self, expected_2, 'Find google search image')
