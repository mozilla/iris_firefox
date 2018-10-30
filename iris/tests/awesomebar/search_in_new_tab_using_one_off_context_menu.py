# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This test case verifies that \'Search in New Tab\' option works correctly using an one-off.'
        self.test_case_id = '108250'
        self.test_suite_id = '1902'
        self.locales = ['en-US']

    def run(self):
        moz_pattern = Pattern('moz.png')
        url = LocalWeb.FIREFOX_TEST_SITE
        google_one_off_button_pattern = Pattern('google_one_off_button.png')
        twitter_one_off_button_highlight_pattern = Pattern('twitter_one_off_button_highlight.png')
        set_as_default_search_engine_pattern = Pattern('set_as_default_search_engine.png')
        search_in_new_tab_pattern = Pattern('search_in_new_tab.png')
        new_tab_twitter_search_results_pattern = Pattern('new_tab_twitter_search_results.png')
        new_tab_twitter_search_results_2_pattern = Pattern('new_tab_twitter_search_results_2.png')

        region = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        select_location_bar()
        paste('moz')

        expected = region.exists(moz_pattern, 10)
        assert_true(self, expected, 'Searched string found at the bottom of the drop-down list.')

        hover(google_one_off_button_pattern)

        try:
            expected = region.wait_vanish(moz_pattern, 10)
            assert_true(self, expected, 'The \'Google\' one-off button is highlighted.')
        except FindError:
            raise FindError('The \'Google\' one-off button is not highlighted.')

        repeat_key_up(3)
        key_to_one_off_search(twitter_one_off_button_highlight_pattern)

        expected = region.exists(twitter_one_off_button_highlight_pattern, 10)
        assert_true(self, expected, 'The \'Twitter\' one-off button is highlighted.')

        right_click(twitter_one_off_button_highlight_pattern)

        expected = exists(search_in_new_tab_pattern, 10)
        assert_true(self, expected, 'The \'Search in New Tab\' option found.')

        expected = exists(set_as_default_search_engine_pattern, 10)
        assert_true(self, expected, 'The \'Set As Default Search Engine\' option found.')

        click(search_in_new_tab_pattern)
        time.sleep(DEFAULT_UI_DELAY_LONG)

        next_tab()

        expected = exists(new_tab_twitter_search_results_pattern, 10) or exists(
            new_tab_twitter_search_results_2_pattern, 5)
        assert_true(self, expected, 'A new tab with the Twitter search results is opened.')
