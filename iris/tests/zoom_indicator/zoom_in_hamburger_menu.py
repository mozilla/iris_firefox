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
        url2 = 'en.wikipedia.org'
        search_bar = 'search_bar.png'
        search_bar_wikipedia_default_zoom_level = 'search_bar_wikipedia_default_zoom_level.png'
        hamburger_menu = 'hamburger_menu.png'
        hamburger_menu_zoom_indicator = 'hamburger_menu_zoom_indicator.png'
        zoom_control_toolbar_increase = 'zoom_control_toolbar_increase.png'
        zoom_control_110_hamburger_menu = 'zoom_control_110_hamburger_menu.png'
        search_bar_wikipedia_110_zoom_level = 'search_bar_wikipedia_110_zoom_level.png'

        # Check that zoom level is not displayed in the url bar for the default page that opens when the browser starts.
        navigate(url1)

        expected = exists(hamburger_menu, 10)
        assert_true(self, expected, 'Page successfully loaded, hamburger menu found.')

        region = create_region_for_url_bar()

        expected = region.exists(search_bar, 10)
        assert_true(self, expected, 'Zoom level not displayed by default in the url bar.')

        # Check that zoom level is not displayed in the url bar for a new opened page.
        navigate(url2)

        expected = exists(hamburger_menu, 10)
        assert_true(self, expected, 'Page successfully loaded, hamburger menu found.')

        expected = region.exists(search_bar_wikipedia_default_zoom_level, 10)
        assert_true(self, expected, 'Zoom level not displayed by default in the url bar.')

        new_region = create_region_for_hamburger_menu()

        expected = new_region.exists(hamburger_menu_zoom_indicator, 10)
        assert_true(self, expected, 'Zoom level is 100% by default.')

        click(zoom_control_toolbar_increase)

        expected = new_region.exists(zoom_control_110_hamburger_menu, 10)
        assert_true(self, expected, 'Zoom controls are correctly displayed in the hamburger menu after increase.')

        # Click the hamburger menu in order to close it.
        # Verify that the zoom level is still increased by checking the page's zoom level from the url bar.
        click(hamburger_menu)

        expected = region.exists(search_bar_wikipedia_110_zoom_level, 10)
        assert_true(self, expected, 'Zoom controls are correctly displayed in the url bar after the increase.')
