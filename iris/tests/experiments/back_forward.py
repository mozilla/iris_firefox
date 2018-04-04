# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *


class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        self.meta = "This is a test of browser back/forward"

    def run(self):
        url = "about:home"
        search_the_web_image = "search_the_web.png"
        google_search_image = "google_search.png"
        back_button_image = "back.png"
        forward_button_image = "forward.png"

        # helper function from "keyboard_shortcuts"
        navigate(url)

        expected_1 = exists(search_the_web_image, 0.5)
        assert_true(self, expected_1, 'Find search the web image')

        navigate("https://www.google.com/?hl=EN")

        expected_2 = exists(google_search_image, 0.5)
        assert_true(self, expected_2, 'Find google search image')

        wait(back_button_image)
        click(back_button_image)

        assert_true(self, expected_1, 'Find search the web image')

        wait(forward_button_image)
        click(forward_button_image)
        assert_true(self, expected_2, 'Find google search image')
