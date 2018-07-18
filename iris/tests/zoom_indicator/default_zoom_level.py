# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that checks the default zoom level'
        self.test_case_id = '7442'
        self.test_suite_id = '242'

    def run(self):
        url = LocalWeb.FIREFOX_TEST_SITE
        url_bar_default_zoom_level = 'url_bar_default_zoom_level.png'
        edit_buttons_below_zoom_buttons = 'edit_buttons_below_zoom_buttons.png'

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        region = create_region_for_url_bar()

        expected = region.exists(url_bar_default_zoom_level, 10)
        assert_true(self, expected, 'Zoom level not displayed by default in the url bar.')

        new_region = create_region_for_hamburger_menu()

        expected = new_region.exists('100%', 10)
        assert_true(self, expected, 'Zoom level is 100% by default.')

        expected = new_region.exists(edit_buttons_below_zoom_buttons, 10, 0.25)
        assert_true(self, expected, 'Control buttons for zooming appear above the Cut/Copy/Paste buttons.')
