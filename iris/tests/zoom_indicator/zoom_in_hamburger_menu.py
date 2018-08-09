# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that checks the zoom in functionality from the hamburger menu.'

    def run(self):
        url1 = 'about:home'
        url2 = LocalWeb.FIREFOX_TEST_SITE
        search_bar_pattern = Pattern('search_bar.png')
        url_bar_default_zoom_level_pattern = Pattern('url_bar_default_zoom_level.png')
        hamburger_menu_zoom_indicator_pattern = Pattern('hamburger_menu_zoom_indicator.png')
        zoom_control_toolbar_increase_pattern = Pattern('zoom_control_toolbar_increase.png')
        url_bar_110_zoom_level_pattern = Pattern('url_bar_110_zoom_level.png')
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
        assert_true(self, expected,
                    'Zoom indicator is correctly displayed in hamburger menu after zoom level is increased.')

        click(hamburger_menu_pattern)

        new_reg = create_region_for_url_bar()
        expected = new_reg.exists(url_bar_110_zoom_level_pattern, 10)
        assert_true(self, expected,
                    'Zoom indicator is correctly displayed in the url bar after zoom level is increased.')
