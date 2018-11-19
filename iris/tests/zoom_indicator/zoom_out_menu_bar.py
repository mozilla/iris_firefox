# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This is a test case that checks the zoom out functionality from the menu bar.'
        self.test_case_id = '7459'
        self.test_suite_id = '242'
        self.locales = ['en-US']

    def run(self):
        url = LocalWeb.FIREFOX_TEST_SITE
        url_bar_default_zoom_level_pattern = LocationBar.URL_BAR_DEFAULT_ZOOM_LEVEL
        urlbar_zoom_button_90_pattern = LocationBar.URLBAR_ZOOM_BUTTON_90

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        select_location_bar()
        expected = exists(url_bar_default_zoom_level_pattern, 10)
        assert_true(self, expected, 'Zoom indicator not displayed by default in the url bar.')

        select_zoom_menu_option(Option.ZOOM_OUT)

        region = create_region_for_url_bar()
        expected = region.exists(urlbar_zoom_button_90_pattern, 10)
        assert_true(self, expected, 'Zoom level successfully decreased, zoom indicator found in the url bar.')
