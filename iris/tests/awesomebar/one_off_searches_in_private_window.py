# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This test case perform one-offs searches in private browsing.'
        self.test_case_id = '108253'
        self.test_suite_id = '1902'
        self.locales = ['en-US']

    def run(self):
        moz_pattern = Pattern('moz.png')
        url = LocalWeb.FIREFOX_TEST_SITE
        search_settings_pattern = Pattern('search_settings.png')
        twitter_one_off_button_highlight_pattern = Pattern('twitter_one_off_button_highlight.png')
        new_tab_twitter_search_results_pattern = Pattern('new_tab_twitter_search_results.png')
        new_tab_twitter_search_results_pattern2 = Pattern('new_tab_twitter_search_results_2.png')
        google_on_off_button_private_window_pattern = Pattern('google_on_off_button_private_window.png')
        magnifying_glass_pattern = Pattern('magnifying_glass.png')
        test_pattern = Pattern('test.png')

        new_private_window()

        navigate(url)

        region = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        select_location_bar()
        paste('moz')

        expected = region.exists(moz_pattern, 10)
        assert_true(self, expected, 'Searched string found at the bottom of the drop-down list.')

        expected = region.exists(search_settings_pattern, 10)
        assert_true(self, expected, 'The \'Search settings\' button is displayed in the awesome bar.')

        repeat_key_up(3)
        key_to_one_off_search(twitter_one_off_button_highlight_pattern, )

        expected = region.exists(twitter_one_off_button_highlight_pattern, 10)
        assert_true(self, expected, 'The \'Twitter\' one-off button is highlighted.')

        type(Key.ENTER)
        time.sleep(DEFAULT_UI_DELAY_LONG)

        expected = exists(new_tab_twitter_search_results_pattern, 10) \
            or exists(new_tab_twitter_search_results_pattern2, 5)
        assert_true(self, expected, 'Twitter search results are opened in the same tab.')

        new_tab()
        time.sleep(DEFAULT_UI_DELAY)

        select_location_bar()
        paste('test')

        expected = region.exists(google_on_off_button_private_window_pattern, 10)
        assert_true(self, expected, 'The\'Google\' one-off button found.')

        if Settings.get_os() == Platform.MAC:
            key_down(Key.CMD)
        else:
            key_down(Key.CTRL)

        click(google_on_off_button_private_window_pattern)

        if Settings.get_os() == Platform.MAC:
            key_up(Key.CMD)
        else:
            key_up(Key.CTRL)

        next_tab()

        expected = region.exists(magnifying_glass_pattern, 10)
        assert_true(self, expected, 'Page successfully loaded using the \'Google\' engine.')

        expected = region.exists(test_pattern, 10)
        assert_true(self, expected,
                    'Searched item is successfully found in the page opened by the \'Google\' search engine.')

        close_window()
