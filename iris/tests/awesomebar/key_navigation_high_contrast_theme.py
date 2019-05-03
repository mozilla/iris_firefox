# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This test case performs key navigation in the URL drop-down in high contrast theme.'
        self.test_case_id = '120136'
        self.test_suite_id = '1902'
        self.locales = ['en-US']

    def run(self):
        url = LocalWeb.FIREFOX_TEST_SITE
        wear_theme_pattern = Pattern('wear_theme.png')
        moz_search_highlight_dark_theme_pattern = Pattern('moz_search_highlight_dark_theme.png')
        search_wikipedia_dark_theme_pattern = Pattern('search_wikipedia_dark_theme.png')

        region = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        open_addons()

        expected = region.exists(AboutAddons.THEMES, 10)
        assert_true(self, expected, 'Add-ons page successfully loaded.')

        click(AboutAddons.THEMES)

        expected = exists(AboutAddons.Themes.DARK_THEME, 10)
        assert_true(self, expected, 'Dark theme option found in the page.')

        right_click(AboutAddons.Themes.DARK_THEME)

        expected = exists(wear_theme_pattern, 10)
        assert_true(self, expected, 'The \'Wear theme\' option found in the page.')

        # Select the 'Wear theme' option.
        click(wear_theme_pattern)

        # Check that 'Wear theme' option successfully selected.
        right_click(AboutAddons.Themes.DARK_THEME)

        try:
            expected = region.wait_vanish(wear_theme_pattern, 10)
            assert_true(self, expected, 'The \'Wear theme\' option not found in the page.')
        except FindError:
            raise FindError('The \'Wear theme\' option found in the page.')

        type(Key.ESC)

        select_location_bar()
        paste('moz')
        type(Key.SPACE)

        expected = region.exists(moz_search_highlight_dark_theme_pattern, 10)
        assert_true(self, expected, 'The searched string is highlighted.')

        # Wait a moment for the suggests list to fully populate before stepping down through it.
        time.sleep(Settings.UI_DELAY)

        repeat_key_up(2)
        key_to_one_off_search(search_wikipedia_dark_theme_pattern)

        expected = region.exists(search_wikipedia_dark_theme_pattern, 10)
        assert_true(self, expected, 'The \'Wikipedia\' one-off button is highlighted.')

        max_attempts = 16

        while max_attempts > 0:
            scroll_up()
            if exists(moz_search_highlight_dark_theme_pattern, 1):
                max_attempts = 0
            max_attempts -= 1

        expected = region.exists(moz_search_highlight_dark_theme_pattern, 10)
        assert_true(self, expected, 'The searched string is highlighted.')
