# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This test case checks the zoom indicator animation using the mousewheel.'

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

        click(LocalWeb.FIREFOX_LOGO)

        # zoom in ONE time.
        zoom_with_mouse_wheel(1, ZoomType.IN)

        new_region = create_region_for_url_bar()

        expected = new_region.exists(url_bar_110_zoom_level, 10)
        assert_true(self, expected, 'Zoom level successfully increased, zoom controls found in the url bar.')

        restart_firefox(self.app.fx_path, self.profile_path, url=LocalWeb.FIREFOX_TEST_SITE)

        expected = new_region.exists(url_bar_110_zoom_level, 10)
        assert_true(self, expected, 'Zoom level successfully increased, zoom controls found in the url bar.')

        # zoom out ONE time.
        zoom_with_mouse_wheel(1, ZoomType.OUT)

        if Settings.get_os() == Platform.MAC:
            select_location_bar()

        expected = new_region.exists(url_bar_default_zoom_level, 10, 0.92)
        assert_true(self, expected, 'Zoom controls not found in the url bar after browser restore its zoom level.')

        # zoom in until the maximum zoom level(300%) is reached.
        zoom_with_mouse_wheel(20, ZoomType.IN)

        expected = new_region.exists(url_bar_300_zoom_level, 10)
        assert_true(self, expected, 'Zoom level successfully increased, maximum zoom level(300%) reached.')

        # zoom in ONE more time.
        zoom_with_mouse_wheel(1, ZoomType.IN)

        expected = new_region.exists(url_bar_300_zoom_level, 10)
        assert_true(self, expected, 'Zoom level still displays 300%.')

        # zoom out until the default zoom level(100%) is reached.
        restore_zoom()

        expected = new_region.exists(url_bar_default_zoom_level, 10, 0.92)
        assert_true(self, expected, 'Zoom controls not found in the url bar after browser restore its zoom level.')

        # zoom out until de minimum zoom level(30%) is reached.
        zoom_with_mouse_wheel(7, ZoomType.OUT)

        expected = new_region.exists(url_bar_30_zoom_level, 10)
        assert_true(self, expected, 'Zoom level successfully decreased, minimum zoom level(30%) reached.')

        # zoom out ONE more time.
        zoom_with_mouse_wheel(1, ZoomType.OUT)

        expected = new_region.exists(url_bar_30_zoom_level, 10)
        assert_true(self, expected, 'Zoom level still displays 30%.')
