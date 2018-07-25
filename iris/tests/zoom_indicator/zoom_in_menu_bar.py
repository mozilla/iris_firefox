# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that checks the zoom in functionality from the menu bar.'
        self.test_case_id = '7455'
        self.test_suite_id = '242'

    def run(self):
        url = LocalWeb.FIREFOX_TEST_SITE
        url_bar_default_zoom_level = 'url_bar_default_zoom_level.png'
        url_bar_110_zoom_level = 'url_bar_110_zoom_level.png'
        hamburger_menu = 'hamburger_menu.png'

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        expected = exists(url_bar_default_zoom_level, 10)
        assert_true(self, expected, 'Zoom level not displayed by default in the url bar.')

        select_zoom_menu_option(Option.ZOOM_IN)

        region = create_region_for_url_bar()

        expected = region.exists(url_bar_110_zoom_level, 10)
        assert_true(self, expected, 'Zoom level successfully increased, zoom controls found in the url bar.')

        # Reset the zoom level from the location bar.
        click(Pattern(hamburger_menu).target_offset(-320, 15))

        expected = region.exists(url_bar_default_zoom_level, 10, 0.92)
        assert_true(self, expected, 'Zoom level not displayed in the url bar after zoom level reset.')
