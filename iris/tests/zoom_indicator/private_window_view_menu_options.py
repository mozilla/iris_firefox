# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that checks the zoom level in a private window when applying the View Menu ' \
                    'Options.'

    def run(self):
        url = LocalWeb.FIREFOX_TEST_SITE
        url_bar_default_zoom_level = 'url_bar_default_zoom_level.png'
        url_bar_110_zoom_level = 'url_bar_110_zoom_level.png'
        url_bar_90_zoom_level = 'url_bar_90_zoom_level.png'
        zoom_text_only_check = 'zoom_text_only_check.png'
        hamburger_menu = 'hamburger_menu.png'

        new_private_window()

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

        select_zoom_menu_option(Option.ZOOM_OUT)

        expected = region.exists(url_bar_90_zoom_level, 10)
        assert_true(self, expected, 'Zoom level successfully decreased, zoom controls found in the url bar.')

        # Reset the zoom level from the location bar.
        click(Pattern(hamburger_menu).target_offset(-320, 15))

        expected = region.exists(url_bar_default_zoom_level, 10, 0.92)
        assert_true(self, expected, 'Zoom level not displayed in the url bar after zoom level reset.')

        select_zoom_menu_option(Option.ZOOM_TEXT_ONLY)

        open_zoom_menu()

        expected = exists(zoom_text_only_check, 10)
        assert_true(self, expected, '\'Zoom text only\' option successfully checked.')

        close_find()
        close_find()

        select_location_bar()

        expected = exists(url_bar_default_zoom_level, 10, 0.92)
        assert_true(self, expected,
                    'Zoom level not displayed in the url bar after \'zoom text only\' option is set.')

        zoom_in()

        expected = region.exists(url_bar_110_zoom_level, 10)
        assert_true(self, expected, 'Zoom level successfully increased, zoom controls found in the url bar.')

        # Reset the zoom level from the location bar.
        click(Pattern(hamburger_menu).target_offset(-320, 15))

        expected = region.exists(url_bar_default_zoom_level, 10, 0.92)
        assert_true(self, expected, 'Zoom level not displayed in the url bar after zoom level reset.')

        zoom_out()

        expected = region.exists(url_bar_90_zoom_level, 10)
        assert_true(self, expected, 'Zoom level successfully decreased, zoom controls found in the url bar.')

        select_zoom_menu_option(Option.RESET)

        expected = region.exists(url_bar_default_zoom_level, 10, 0.92)
        assert_true(self, expected,
                    'Zoom level not displayed in the url bar after zoom level reset.')

        open_zoom_menu()

        expected = exists(zoom_text_only_check, 10)
        assert_true(self, expected, '\'Zoom text only\' option is still checked.')

        close_find()
        close_find()
