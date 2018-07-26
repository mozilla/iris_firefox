# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that checks the zoom reset functionality from the hamburger menu.'

    def run(self):
        url1 = 'about:home'
        url2 = LocalWeb.FIREFOX_TEST_SITE
        search_bar = 'search_bar.png'
        url_bar_default_zoom_level = 'url_bar_default_zoom_level.png'
        hamburger_menu = 'hamburger_menu.png'
        hamburger_menu_zoom_indicator = 'hamburger_menu_zoom_indicator.png'
        zoom_control_toolbar_increase = 'zoom_control_toolbar_increase.png'
        zoom_control_110 = 'zoom_control_110.png'
        url_bar_110_zoom_level = 'url_bar_110_zoom_level.png'

        # Check that zoom level is not displayed in the url bar for the default page that opens when the browser starts.
        navigate(url1)

        expected = exists(hamburger_menu, 10)
        assert_true(self, expected, 'Page successfully loaded, hamburger menu found.')

        expected = exists(search_bar, 10)
        assert_true(self, expected, 'Zoom level not displayed by default in the url bar.')

        # Check that zoom level is not displayed in the url bar for a new opened page.
        navigate(url2)

        expected = exists(hamburger_menu, 10)
        assert_true(self, expected, 'Page successfully loaded, hamburger menu found.')

        region = create_region_for_url_bar()

        expected = region.exists(url_bar_default_zoom_level, 10)
        assert_true(self, expected, 'Zoom level not displayed by default in the url bar.')

        new_region = create_region_for_hamburger_menu()

        expected = new_region.exists(hamburger_menu_zoom_indicator, 10)
        assert_true(self, expected, 'Zoom level is 100% by default.')

        click(zoom_control_toolbar_increase)

        expected = new_region.exists(zoom_control_110, 10)
        assert_true(self, expected, 'Zoom level is correctly displayed in the hamburger menu after zoom increase.')

        # Click the hamburger menu in order to close it.
        click(hamburger_menu)

        new_reg = create_region_for_url_bar()

        expected = new_reg.exists(url_bar_110_zoom_level, 10)
        assert_true(self, expected, 'Zoom level is correctly displayed in the url bar after zoom increase.')

        # Open hamburger menu and reset the zoom level.
        click(hamburger_menu)
        click(Pattern(zoom_control_toolbar_increase).target_offset(-40, 15))

        expected = new_region.exists(hamburger_menu_zoom_indicator, 10)
        assert_true(self, expected, 'Zoom level is successfully reset to default in hamburger menu.')

        expected = region.exists(url_bar_default_zoom_level, 10)
        assert_true(self, expected, 'Zoom level is displayed anymore in the url bar.')
