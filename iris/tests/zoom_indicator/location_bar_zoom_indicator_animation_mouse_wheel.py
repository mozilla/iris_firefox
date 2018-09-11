# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This test case checks the zoom indicator animation from the url bar using the mousewheel.'
        self.test_case_id = '7446'
        self.test_suite_id = '242'

    def run(self):
        url = LocalWeb.FIREFOX_TEST_SITE
        url_bar_default_zoom_level_pattern = Pattern('url_bar_default_zoom_level.png')
        url_bar_30_zoom_level_pattern = Pattern('url_bar_30_zoom_level.png').similar(0.7)
        url_bar_110_zoom_level_pattern = Pattern('url_bar_110_zoom_level.png')
        url_bar_300_zoom_level_pattern = Pattern('url_bar_300_zoom_level.png')

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        region = create_region_for_url_bar()

        expected = region.exists(url_bar_default_zoom_level_pattern.similar(0.92), 10)
        assert_true(self, expected, 'Zoom indicator not displayed by default in the url bar.')

        click(LocalWeb.FIREFOX_LOGO)

        zoom_with_mouse_wheel(1, ZoomType.IN)

        new_region = create_region_for_url_bar()

        expected = new_region.exists(url_bar_110_zoom_level_pattern, 10)
        assert_true(self, expected, 'Zoom level successfully increased, zoom indicator found in the url bar.')

        restart_firefox(self.app.fx_path, self.profile_path, url=LocalWeb.FIREFOX_TEST_SITE)

        expected = new_region.exists(url_bar_110_zoom_level_pattern, 10)
        assert_true(self, expected, 'Zoom level successfully increased, zoom indicator found in the url bar.')

        zoom_with_mouse_wheel(1, ZoomType.OUT)

        select_location_bar()

        expected = new_region.exists(url_bar_default_zoom_level_pattern.similar(0.92), 10)
        assert_true(self, expected, 'Zoom controls not found in the url bar after browser restore its zoom level.')

        zoom_with_mouse_wheel(20, ZoomType.IN)

        expected = new_region.exists(url_bar_300_zoom_level_pattern, 10)
        assert_true(self, expected, 'Zoom level successfully increased, maximum zoom level (300%) reached.')

        zoom_with_mouse_wheel(1, ZoomType.IN)

        expected = new_region.exists(url_bar_300_zoom_level_pattern, 10)
        assert_true(self, expected, 'Zoom indicator still displays 300%.')

        # zoom out until the default zoom level(100%) is reached.
        restore_zoom()

        expected = new_region.exists(url_bar_default_zoom_level_pattern.similar(0.92), 10)
        assert_true(self, expected, 'Zoom indicator not found in the url bar after browser restore its zoom level.')

        # zoom out until de minimum zoom level(30%) is reached.
        zoom_with_mouse_wheel(7, ZoomType.OUT)

        expected = new_region.exists(url_bar_30_zoom_level_pattern, 10)
        assert_true(self, expected, 'Zoom level successfully decreased, minimum zoom level (30%) reached.')

        # zoom out ONE more time.
        zoom_with_mouse_wheel(1, ZoomType.OUT)

        expected = new_region.exists(url_bar_30_zoom_level_pattern, 10)
        assert_true(self, expected, 'Zoom indicator still displays 30%.')
