# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that resets the zoom level from the menu bar.'

    def run(self):
        url = LocalWeb.FIREFOX_TEST_SITE
        url_bar_default_zoom_level = 'url_bar_default_zoom_level.png'
        url_bar_110_zoom_level = 'url_bar_110_zoom_level.png'

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        expected = exists(url_bar_default_zoom_level, 10)
        assert_true(self, expected, 'Zoom indicator not displayed by default in the url bar.')

        select_zoom_menu_option(Option.ZOOM_IN)

        expected = exists(url_bar_110_zoom_level, 10)
        assert_true(self, expected, 'Zoom level successfully increased, zoom indicator found in the url bar.')

        # Reset the zoom level from the menu bar.
        select_zoom_menu_option(Option.RESET)

        region = create_region_for_url_bar()

        expected = region.exists(Pattern(url_bar_default_zoom_level).similar(0.92), 10)
        assert_true(self, expected, 'Zoom indicator not displayed in the url bar after zoom level reset.')
