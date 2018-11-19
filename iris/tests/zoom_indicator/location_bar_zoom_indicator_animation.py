# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This test case checks the zoom indicator animation from the url bar.'
        self.test_case_id = '7451'
        self.test_suite_id = '242'
        self.locales = ['en-US', 'zh-CN', 'es-ES', 'de', 'fr', 'ru', 'ko', 'pt-PT', 'vi', 'pl', 'tr', 'ro', 'ja']

    def run(self):
        url = LocalWeb.FIREFOX_TEST_SITE
        url_bar_default_zoom_level_pattern = LocationBar.URL_BAR_DEFAULT_ZOOM_LEVEL
        urlbar_zoom_button_30_pattern = LocationBar.URLBAR_ZOOM_BUTTON_30.similar(0.7)
        urlbar_zoom_button_110_pattern = LocationBar.URLBAR_ZOOM_BUTTON_110
        urlbar_zoom_button_300_pattern = LocationBar.URLBAR_ZOOM_BUTTON_300

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        region = create_region_for_url_bar()

        expected = region.exists(url_bar_default_zoom_level_pattern.similar(0.92), 10)
        assert_true(self, expected, 'Zoom indicator not displayed by default in the url bar.')

        zoom_in()

        new_region = create_region_for_url_bar()

        expected = new_region.exists(urlbar_zoom_button_110_pattern, 10)
        assert_true(self, expected, 'Zoom level successfully increased, zoom indicator found in the url bar.')

        restart_firefox(self,
                        self.browser.path,
                        self.profile_path,
                        LocalWeb.FIREFOX_TEST_SITE,
                        image=LocalWeb.FIREFOX_LOGO)

        expected = new_region.exists(urlbar_zoom_button_110_pattern, 10)
        assert_true(self, expected, 'Zoom controls still displayed in the url bar after browser restart.')

        zoom_out()

        select_location_bar()

        expected = new_region.exists(url_bar_default_zoom_level_pattern.similar(0.92), 10)
        assert_true(self, expected, 'Zoom level successfully decreased, zoom indicator not found in the url bar for '
                                    '100% zoom level.')

        for i in range(8):
            zoom_in()

        expected = new_region.exists(urlbar_zoom_button_300_pattern, 10)
        assert_true(self, expected, 'Zoom level successfully increased, maximum zoom level(300%) reached.')

        zoom_in()

        expected = new_region.exists(urlbar_zoom_button_300_pattern, 10)
        assert_true(self, expected, 'Zoom indicator still displays 300%.')

        for i in range(8):
            zoom_out()

        expected = new_region.exists(url_bar_default_zoom_level_pattern.similar(0.92), 10)
        assert_true(self, expected, 'Zoom level successfully decreased, zoom indicator not found in the url bar for '
                                    '100% zoom level.')

        for i in range(5):
            zoom_out()

        expected = new_region.exists(urlbar_zoom_button_30_pattern, 10)
        assert_true(self, expected, 'Zoom level successfully decreased, minimum zoom level(30%) reached.')

        zoom_out()

        expected = new_region.exists(urlbar_zoom_button_30_pattern, 10)
        assert_true(self, expected, 'Zoom indicator still displays 30%.')
