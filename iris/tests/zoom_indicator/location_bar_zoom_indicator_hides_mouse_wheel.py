# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This test case checks that zoom indicator hides in the location bar; zoom is performed using the' \
                    ' mouse wheel.'
        self.test_case_id = '7452'
        self.test_suite_id = '242'

    def run(self):
        url = LocalWeb.FIREFOX_TEST_SITE
        url_bar_default_zoom_level_pattern = Pattern('url_bar_default_zoom_level.png')
        url_bar_110_zoom_level_pattern = Pattern('url_bar_110_zoom_level.png')
        url_bar_90_zoom_level_pattern = Pattern('url_bar_90_zoom_level.png').similar(0.7)

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        region = create_region_for_url_bar()

        expected = region.exists(url_bar_default_zoom_level_pattern.similar(0.92), 10)
        assert_true(self, expected, 'Zoom indicator not displayed by default in the url bar.')

        click(LocalWeb.FIREFOX_LOGO)
        zoom_with_mouse_wheel(1, ZoomType.IN)

        new_region = create_region_for_url_bar()
        click(NavBar.HAMBURGER_MENU.target_offset(-170, 15))

        expected = new_region.exists(url_bar_110_zoom_level_pattern, 10)
        assert_true(self, expected, 'Zoom level successfully increased, zoom indicator found in the url bar.')

        zoom_with_mouse_wheel(1, ZoomType.OUT)

        expected = new_region.exists(url_bar_default_zoom_level_pattern.similar(0.92), 10)
        assert_true(self, expected,
                    'Zoom level successfully decreased, zoom indicator not found in the url bar for 100%'
                    ' zoom level.')

        zoom_with_mouse_wheel(1, ZoomType.OUT)

        expected = new_region.exists(url_bar_90_zoom_level_pattern, 10)
        assert_true(self, expected, 'Zoom level successfully decreased, zoom indicator found in the url bar.')

        zoom_with_mouse_wheel(1, ZoomType.IN)

        expected = new_region.exists(url_bar_default_zoom_level_pattern.similar(0.92), 10)
        assert_true(self, expected, 'Zoom level successfully increased, zoom indicator not found in the url bar.')
