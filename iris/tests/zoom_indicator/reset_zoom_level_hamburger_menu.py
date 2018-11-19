# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This is a test case that checks the zoom level reset functionality from the hamburger menu.'
        self.test_case_id = '7457'
        self.test_suite_id = '242'
        self.locales = ['en-US']

    def run(self):
        url1 = 'about:home'
        url2 = LocalWeb.FIREFOX_TEST_SITE
        search_bar_pattern = LocationBar.SEARCH_BAR
        url_bar_default_zoom_level_pattern = LocationBar.URL_BAR_DEFAULT_ZOOM_LEVEL
        hamburger_menu_zoom_indicator_pattern = HamburgerMenu.HAMBURGER_MENU_ZOOM_INDICATOR
        zoom_control_toolbar_increase_pattern = NavBar.ZOOM_IN
        urlbar_zoom_button_110_pattern = LocationBar.URLBAR_ZOOM_BUTTON_110
        hamburger_menu_pattern = NavBar.HAMBURGER_MENU

        navigate(url1)

        expected = exists(hamburger_menu_pattern, 10)
        assert_true(self, expected, 'Page successfully loaded, hamburger menu found.')

        expected = exists(search_bar_pattern, 10)
        assert_true(self, expected, 'Zoom indicator not displayed by default in the url bar.')

        navigate(url2)

        expected = exists(hamburger_menu_pattern, 10)
        assert_true(self, expected, 'Page successfully loaded, hamburger menu found.')

        region = create_region_for_url_bar()

        expected = region.exists(url_bar_default_zoom_level_pattern, 10)
        assert_true(self, expected, 'Zoom indicator not displayed by default in the url bar.')

        new_region = create_region_for_hamburger_menu()

        expected = new_region.exists(hamburger_menu_zoom_indicator_pattern, 10)
        assert_true(self, expected, 'By default zoom indicator is 100% in hamburger menu.')

        click(zoom_control_toolbar_increase_pattern)

        expected = new_region.exists('110%', 10)
        assert_true(self, expected, 'Zoom indicator is correctly displayed in hamburger menu after zoom level is '
                                    'increased.')

        click(hamburger_menu_pattern)

        new_reg = create_region_for_url_bar()

        expected = new_reg.exists(urlbar_zoom_button_110_pattern, 10)
        assert_true(self, expected,
                    'Zoom indicator is correctly displayed in the url bar after zoom level is increased.')

        click(hamburger_menu_pattern)
        click(zoom_control_toolbar_increase_pattern.target_offset(-40, 10))

        select_location_bar()

        expected = new_region.exists(hamburger_menu_zoom_indicator_pattern, 10)
        assert_true(self, expected, 'Zoom indicator is successfully reset to default in hamburger menu.')

        if Settings.get_os() == Platform.WINDOWS or Settings.get_os() == Platform.LINUX:
            expected = region.exists(url_bar_default_zoom_level_pattern.similar(0.95), 10)
            assert_true(self, expected, 'Zoom indicator is displayed anymore in the url bar.')
        else:
            expected = region.exists(url_bar_default_zoom_level_pattern.similar(0.93), 10)
            assert_true(self, expected, 'Zoom indicator is displayed anymore in the url bar.')
