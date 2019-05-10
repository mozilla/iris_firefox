# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
            description='This test case performs key navigation in the URL drop-down in high contrast theme.',
            locale=['en-US'],
            test_case_id='120136',
            test_suite_id='1902'
        )
    def run(self, firefox):
        url = LocalWeb.FIREFOX_TEST_SITE
        themes_pattern = Pattern('themes.png')
        dark_theme_pattern = Pattern('dark_theme.png')
        wear_theme_pattern = Pattern('wear_theme.png')
        moz_search_highlight_dark_theme_pattern = Pattern('moz_search_highlight_dark_theme.png')
        search_wikipedia_dark_theme_pattern = Pattern('search_wikipedia_dark_theme.png')

        region = Region(0, 0, Screen().width, 2*Screen().height / 3)

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert expected, 'Page successfully loaded, firefox logo found.'

        open_addons()

        expected = region.exists(themes_pattern, 10)
        assert expected, 'Add-ons page successfully loaded.'

        click(themes_pattern)

        expected = exists(dark_theme_pattern, 10)
        assert expected, 'Dark theme option found in the page.'

        right_click(dark_theme_pattern)

        expected = exists(wear_theme_pattern, 10)
        assert expected, 'The \'Wear theme\' option found in the page.'

        # Select the 'Wear theme' option.
        click(wear_theme_pattern)

        # Check that 'Wear theme' option successfully selected.
        right_click(dark_theme_pattern)
        # try:
        #     expected = region.exists(stop_wear_theme, 10)
        #     assert  expected, 'The \'Wear theme\' option not found in the page.'
        # except FindError:
        #     raise FindError('The \'Wear theme\' option found in the page.')

        type(Key.ESC)

        select_location_bar()
        paste('moz')
        type(Key.SPACE)

        expected = region.exists(moz_search_highlight_dark_theme_pattern, 10)
        assert expected, 'The searched string is highlighted.'

        # Wait a moment for the suggests list to fully populate before stepping down through it.
        time.sleep(Settings.DEFAULT_UI_DELAY)

        repeat_key_up(2)
        key_to_one_off_search(search_wikipedia_dark_theme_pattern)

        expected = region.exists(search_wikipedia_dark_theme_pattern, 10)
        assert expected, 'The \'Wikipedia\' one-off button is highlighted.'

        max_attempts = 16

        while max_attempts > 0:
            scroll_up()
            if exists(moz_search_highlight_dark_theme_pattern, 1):
                max_attempts = 0
            max_attempts -= 1

        expected = region.exists(moz_search_highlight_dark_theme_pattern, 10)
        assert expected, 'The searched string is highlighted.'
