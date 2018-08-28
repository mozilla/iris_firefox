# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This test case performs key navigation in the URL drop-down in high contrast theme.'
        self.test_case_id = '120136'
        self.test_suite_id = '1902'

    def run(self):
        url = LocalWeb.FIREFOX_TEST_SITE
        themes_pattern = Pattern('themes.png')
        dark_theme_pattern = Pattern('dark_theme.png')
        wear_theme_pattern = Pattern('wear_theme.png')
        moz_search_highlight_dark_theme_pattern = Pattern('moz_search_highlight_dark_theme.png')
        search_wikipedia_dark_theme_pattern = Pattern('search_wikipedia_dark_theme.png')

        region = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        click_hamburger_menu_option("Add-ons")

        expected = region.exists(themes_pattern, 10)
        assert_true(self, expected, 'Add-ons page successfully loaded.')

        click(themes_pattern)

        expected = exists(dark_theme_pattern, 10)
        assert_true(self, expected, 'Dark theme option found in the page.')

        right_click(dark_theme_pattern)

        expected = exists(wear_theme_pattern, 10)
        assert_true(self, expected, 'The \'Wear theme\' option found in the page.')

        # Select the 'Wear theme' option.
        click(wear_theme_pattern)

        # Check that 'Wear theme' option successfully selected.
        right_click(dark_theme_pattern)

        try:
            expected = region.wait_vanish(wear_theme_pattern, 10)
            assert_true(self, expected, 'The \'Wear theme\' option not found in the page.')
        except FindError:
            raise FindError('The \'Wear theme\' option found in the page.')

        type(Key.ESC)

        select_location_bar()
        paste('moz')

        expected = region.exists(moz_search_highlight_dark_theme_pattern, 10)
        assert_true(self, expected, 'The searched string is highlighted.')

        for i in range(16):
            scroll_down()

        expected = region.exists(search_wikipedia_dark_theme_pattern, 10)
        assert_true(self, expected, 'The \'Wikipedia\' one-off button is highlighted.')

        for i in range(16):
            scroll_up()

        expected = region.exists(moz_search_highlight_dark_theme_pattern, 10)
        assert_true(self, expected, 'The searched string is highlighted.')
