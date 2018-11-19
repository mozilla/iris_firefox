# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This test case verifies the zoom level on multiple tabs using multiple sites.'
        self.test_case_id = '7448'
        self.test_suite_id = '242'
        self.locales = ['en-US', 'zh-CN', 'es-ES', 'de', 'fr', 'ru', 'ko', 'pt-PT', 'vi', 'pl', 'tr', 'ro', 'ja']

    def run(self):
        url_1 = LocalWeb.FIREFOX_TEST_SITE
        url_2 = LocalWeb.FIREFOX_TEST_SITE_2
        url_bar_default_zoom_level_pattern = LocationBar.URL_BAR_DEFAULT_ZOOM_LEVEL
        urlbar_zoom_button_110_pattern = LocationBar.URLBAR_ZOOM_BUTTON_110

        navigate(url_1)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        region = create_region_for_url_bar()

        expected = region.exists(url_bar_default_zoom_level_pattern, 10)
        assert_true(self, expected, 'Zoom indicator not displayed by default in the url bar.')

        zoom_in()

        expected = exists(urlbar_zoom_button_110_pattern, 10)
        assert_true(self, expected, 'Zoom level successfully increased, zoom indicator found in the url bar.')

        new_tab()

        navigate(url_1)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        expected = exists(urlbar_zoom_button_110_pattern, 10)
        assert_true(self, expected,
                    'Zoom indicator still displays 110% in the new tab opened for the site for which the '
                    'zoom level was set.')

        new_tab()
        navigate(url_2)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        select_location_bar()
        expected = region.exists(url_bar_default_zoom_level_pattern, 10)
        assert_true(self, expected, 'Zoom indicator not displayed in the url bar.')
