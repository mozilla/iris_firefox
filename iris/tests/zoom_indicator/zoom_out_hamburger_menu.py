# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that checks the zoom out functionality from the hamburger menu.'
        self.test_case_id = '7456'
        self.test_suite_id = '242'

    def run(self):
        url1 = 'about:home'
        url2 = LocalWeb.FIREFOX_TEST_SITE
        search_bar = 'search_bar.png'
        url_bar_default_zoom_level = 'url_bar_default_zoom_level.png'
        hamburger_menu = 'hamburger_menu.png'
        hamburger_menu_zoom_indicator = 'hamburger_menu_zoom_indicator.png'
        zoom_control_toolbar_decrease = 'zoom_control_toolbar_decrease.png'
        zoom_control_90 = 'zoom_control_90.png'
        url_bar_90_zoom_level = 'url_bar_90_zoom_level.png'

        # Check that zoom indicator is not displayed in the url bar for the default page that opens when the browser
        # starts.
        navigate(url1)

        expected = exists(hamburger_menu, 10)
        assert_true(self, expected, 'Page successfully loaded, hamburger menu found.')

        expected = exists(search_bar, 10)
        assert_true(self, expected, 'Zoom indicator not displayed by default in the url bar.')

        # Check that zoom indicator is not displayed in the url bar for a new opened page.
        navigate(url2)

        expected = exists(hamburger_menu, 10)
        assert_true(self, expected, 'Page successfully loaded, hamburger menu found.')

        region = create_region_for_url_bar()

        expected = region.exists(url_bar_default_zoom_level, 10)
        assert_true(self, expected, 'Zoom indicator not displayed by default in the url bar.')

        new_region = create_region_for_hamburger_menu()

        expected = new_region.exists(hamburger_menu_zoom_indicator, 10)
        assert_true(self, expected, 'By default zoom indicator is 100% in hamburger menu.')

        click(zoom_control_toolbar_decrease)

        expected = new_region.exists(zoom_control_90, 10)
        assert_true(self, expected,
                    'Zoom indicator is correctly displayed in hamburger menu after zoom level decrease.')

        # Click the hamburger menu in order to close it.
        click(hamburger_menu)

        new_reg = create_region_for_url_bar()

        expected = new_reg.exists(url_bar_90_zoom_level, 10)
        assert_true(self, expected, 'Zoom indicator is correctly displayed in the url bar after zoom level decrease.')
