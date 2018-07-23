# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that checks the \'zoom text only\' functionality.'

    def run(self):
        url = LocalWeb.FIREFOX_TEST_SITE
        url_bar_default_zoom_level = 'url_bar_default_zoom_level.png'
        url_bar_110_zoom_level = 'url_bar_110_zoom_level.png'
        url_bar_90_zoom_level = 'url_bar_90_zoom_level.png'
        view_menu = 'view_menu.png'
        zoom_text_only_check = 'zoom_text_only_check.png'

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        region = create_region_for_url_bar()

        expected = region.exists(url_bar_default_zoom_level, 10)
        assert_true(self, expected, 'Zoom level not displayed by default in the url bar.')

        open_zoom_menu(Option.ZOOM_TEXT_ONLY)

        if Settings.get_os() == Platform.MAC:
            click(view_menu)
            for i in range(3):
                type(text=Key.DOWN)
            type(text=Key.ENTER)
        else:
            type(text='v', modifier=KeyModifier.ALT)
            for i in range(2):
                type(text=Key.DOWN)
            type(text=Key.ENTER)

        expected = exists(zoom_text_only_check, 10)
        assert_true(self, expected, '\'Zoom text only\' functionality successfully checked.')

        close_find()
        close_find()

        expected = region.exists(url_bar_default_zoom_level, 10, 0.92)
        assert_true(self, expected,
                    'Zoom level not displayed in the url bar after \'zoom text only\' functionality is set.')

        zoom_in()

        new_region = create_region_for_url_bar()

        expected = new_region.exists(url_bar_110_zoom_level, 10)
        assert_true(self, expected, 'Zoom level successfully increased, zoom controls found in the url bar.')

        zoom_out()
        zoom_out()

        expected = new_region.exists(url_bar_90_zoom_level, 10)
        assert_true(self, expected, 'Zoom level successfully decreased, zoom controls found in the url bar.')

        open_zoom_menu(Option.RESET)

        expected = new_region.exists(url_bar_default_zoom_level, 10, 0.92)
        assert_true(self, expected,
                    'Zoom level not displayed in the url bar after zoom level reset.')

        if Settings.get_os() == Platform.MAC:
            click(view_menu)
            for i in range(3):
                type(text=Key.DOWN)
            type(text=Key.ENTER)
        else:
            type(text='v', modifier=KeyModifier.ALT)
            for i in range(2):
                type(text=Key.DOWN)
            type(text=Key.ENTER)

        expected = exists(zoom_text_only_check, 10)
        assert_true(self, expected, '\'Zoom text only\' functionality is still checked.')

        close_find()
        close_find()
