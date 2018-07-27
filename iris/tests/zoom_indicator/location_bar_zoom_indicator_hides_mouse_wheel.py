# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This test case checks that zoom indicator hides in the location bar; zoom is performed using the ' \
                    'mouse wheel.'

    def run(self):
        url = LocalWeb.FIREFOX_TEST_SITE
        url_bar_default_zoom_level = 'url_bar_default_zoom_level.png'
        url_bar_110_zoom_level = 'url_bar_110_zoom_level.png'
        url_bar_90_zoom_level = 'url_bar_90_zoom_level.png'
        hamburger_menu = 'hamburger_menu.png'

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        region = create_region_for_url_bar()

        expected = region.exists(url_bar_default_zoom_level, 10, 0.92)
        assert_true(self, expected, 'Zoom indicator not displayed by default in the url bar.')

        click(LocalWeb.FIREFOX_LOGO)

        # zoom in ONE time.
        zoom_with_mouse_wheel(1, ZoomType.IN)

        new_region = create_region_for_url_bar()

        # move focus away from the location bar.
        click(Pattern(hamburger_menu).target_offset(-170, 15))

        expected = new_region.exists(url_bar_110_zoom_level, 10)
        assert_true(self, expected, 'Zoom level successfully increased, zoom indicator found in the url bar.')

        # zoom out ONE time.
        zoom_with_mouse_wheel(1, ZoomType.OUT)

        expected = new_region.exists(url_bar_default_zoom_level, 10, 0.92)
        assert_true(self, expected,
                    'Zoom level successfully decreased, zoom indicator not found in the url bar for 100%'
                    ' zoom level.')

        # zoom out ONE time.
        zoom_with_mouse_wheel(1, ZoomType.OUT)

        expected = new_region.exists(url_bar_90_zoom_level, 10)
        assert_true(self, expected, 'Zoom level successfully decreased, zoom indicator found in the url bar.')

        # zoom in ONE time.
        zoom_with_mouse_wheel(1, ZoomType.IN)

        expected = new_region.exists(url_bar_default_zoom_level, 10, 0.92)
        assert_true(self, expected, 'Zoom level successfully increased, zoom indicator not found in the url bar.')
