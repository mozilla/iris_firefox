# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This is a test case that checks the zoom indicator in a private window when applying keyboard keys.'
        self.test_case_id = '7465'
        self.test_suite_id = '242'
        self.locales = ['en-US']

    def run(self):
        url = LocalWeb.FIREFOX_TEST_SITE
        url_bar_default_zoom_level_pattern = LocationBar.URL_BAR_DEFAULT_ZOOM_LEVEL
        urlbar_zoom_button_90_pattern = LocationBar.URLBAR_ZOOM_BUTTON_90
        urlbar_zoom_button_110_pattern = LocationBar.URLBAR_ZOOM_BUTTON_110
        hamburger_menu_pattern = NavBar.HAMBURGER_MENU

        new_private_window()
        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        region = create_region_for_url_bar()
        select_location_bar()

        expected = region.exists(url_bar_default_zoom_level_pattern, 10)
        assert_true(self, expected, 'Zoom indicator not displayed by default in the url bar.')

        zoom_with_mouse_wheel(1, ZoomType.IN)

        new_region = create_region_for_url_bar()

        expected = new_region.exists(urlbar_zoom_button_110_pattern, 10)
        assert_true(self, expected, 'Zoom level successfully increased, zoom indicator found in the url bar.')

        restore_zoom()

        expected = region.exists(url_bar_default_zoom_level_pattern, 10)
        assert_true(self, expected, 'Zoom indicator not displayed by default in the url bar.')

        new_reg = create_region_for_hamburger_menu()

        expected = new_reg.exists('100%', 10)
        assert_true(self, expected, 'By default zoom indicator is 100% in hamburger menu.')

        click(hamburger_menu_pattern)

        zoom_with_mouse_wheel(1, ZoomType.OUT)

        expected = new_region.exists(urlbar_zoom_button_90_pattern, 10)
        assert_true(self, expected, 'Zoom level successfully decreased, zoom indicator found in the url bar.')

        restore_zoom()

        expected = region.exists(url_bar_default_zoom_level_pattern, 10)
        assert_true(self, expected, 'Zoom indicator not displayed in the url bar after zoom reset.')

        click(hamburger_menu_pattern)
        time.sleep(DEFAULT_UI_DELAY)

        expected = new_reg.exists('100%', 10)
        assert_true(self, expected, 'By default zoom indicator is 100% in hamburger menu.')
