# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This test case checks the zoom indicator animation.'

    def run(self):
        url = LocalWeb.FIREFOX_TEST_SITE
        url_bar_default_zoom_level = 'url_bar_default_zoom_level.png'
        url_bar_30_zoom_level = 'url_bar_30_zoom_level.png'
        url_bar_110_zoom_level = 'url_bar_110_zoom_level.png'
        url_bar_300_zoom_level = 'url_bar_300_zoom_level.png'

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        region = create_region_for_url_bar()

        expected = region.exists(url_bar_default_zoom_level, 10, 0.92)
        assert_true(self, expected, 'Zoom level not displayed by default in the url bar.')

        restart_firefox(self.app.fx_path, self.profile_path, url=LocalWeb.FIREFOX_TEST_SITE)

        expected = region.exists(url_bar_default_zoom_level, 10, 0.92)
        assert_true(self, expected, 'Zoom level not displayed by default in the url bar even after browser restart.')

        zoom_in()

        new_region = create_region_for_url_bar()

        expected = new_region.exists(url_bar_110_zoom_level, 10)
        assert_true(self, expected, 'Zoom level successfully increased, zoom controls found in the url bar.')

        restart_firefox(self.app.fx_path, self.profile_path, url=LocalWeb.FIREFOX_TEST_SITE)

        expected = new_region.exists(url_bar_110_zoom_level, 10)
        assert_true(self, expected, 'Zoom controls still displayed in the url bar after browser restart.')

        zoom_out()

        expected = new_region.exists(url_bar_default_zoom_level, 10, 0.92)
        assert_true(self, expected, 'Zoom level successfully decreased, zoom controls not found in the url bar for 100%'
                                    ' zoom level.')

        restart_firefox(self.app.fx_path, self.profile_path, url=LocalWeb.FIREFOX_TEST_SITE)

        expected = new_region.exists(url_bar_default_zoom_level, 10, 0.92)
        assert_true(self, expected, 'Zoom controls not found in the url bar after browser restart for 100% zoom level.')

        for i in range(8):
            zoom_in()

        expected = new_region.exists(url_bar_300_zoom_level, 10)
        assert_true(self, expected, 'Zoom level successfully increased, maximum zoom level(300%) reached.')

        zoom_in()

        expected = new_region.exists(url_bar_300_zoom_level, 10)
        assert_true(self, expected, 'Zoom level still displays 300%.')

        for i in range(8):
            zoom_out()

        expected = exists(url_bar_default_zoom_level, 10, 0.92)
        assert_true(self, expected, 'Zoom level successfully decreased, zoom controls not found in the url bar for 100%'
                                    ' zoom level.')

        for i in range(5):
            zoom_out()

        expected = new_region.exists(url_bar_30_zoom_level, 10)
        assert_true(self, expected, 'Zoom level successfully decreased, minimum zoom level(30%) reached.')

        zoom_out()

        expected = new_region.exists(url_bar_30_zoom_level, 10)
        assert_true(self, expected, 'Zoom level still displays 30%.')
