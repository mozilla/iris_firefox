# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This is a test of new tab preferences search'
        self.enabled = False

    def run(self):
        url = 'about:home'
        customize_new_tab_page_pattern = Pattern('customize_new_tab_icon.png')
        tab_preference_search_button_pattern = Pattern('tab_preference_search_button.png')
        tab_search_section_pattern = Pattern('search_the_web.png')

        navigate(url)

        expected_1 = exists(customize_new_tab_page_pattern, 10)
        assert_true(self, expected_1, 'Find customize new tab page image')

        click(customize_new_tab_page_pattern)
        expected_2 = exists(tab_preference_search_button_pattern, 10)
        assert_true(self, expected_2, 'Find tab preferences search button')

        click(tab_preference_search_button_pattern)
        new_tab()
        navigate(url)

        expected_3 = wait_vanish(tab_search_section_pattern)
        assert_true(self, expected_3, 'Wait for tab search section to vanish')
