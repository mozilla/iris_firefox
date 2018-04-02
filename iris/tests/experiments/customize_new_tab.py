# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *


class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        self.meta = "This is a test of new tab preferences search"

    def run(self):
        url = "about:home"
        customize_new_tab_page_image = "customize_new_tab_icon.png"
        tab_preference_search_button = "tab_preference_search_button.png"
        tab_search_section = "search_the_web.png"

        navigate(url)

        expected_1 = exists(customize_new_tab_page_image, 0.5)
        assert_true(self, expected_1, 'Find customize new tab page image')

        click(customize_new_tab_page_image)
        expected_2 = exists(tab_preference_search_button, 0.5)
        assert_true(self, expected_2, 'Find tab preferences search button')

        click(tab_preference_search_button)
        expected_3 = waitVanish(tab_search_section)
        assert_false(self, expected_3, 'Wait for tab search section to vanish')
