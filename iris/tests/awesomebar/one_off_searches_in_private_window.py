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
        search_settings_pattern = Pattern('search_settings.png')
        twitter_one_off_button_highlight_pattern = Pattern('twitter_one_off_button_highlight.png')
        new_tab_twitter_search_results_pattern = Pattern('new_tab_twitter_search_results.png')
        new_tab_twitter_search_results_2_pattern = Pattern('new_tab_twitter_search_results_2.png')
        google_on_off_private_window_pattern = Pattern('google_on_off_button_private_window.png')
        magnifying_glass_pattern = Pattern('magnifying_glass.png')
        test_pattern = Pattern('test.png')

        new_private_window()

        private_window_opened = exists(PrivateWindow.private_window_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, private_window_opened, 'A new private window is successfully loaded.')

        # Set English language preference on Google page settings.
        navigate('https://www.google.com/preferences?hl=en-US&fg=1#languages')

        save_button_google_available = exists(Utils.SAVE_BUTTON_GOOGLE, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, save_button_google_available, '\'Save\' google button available.')

        click(Utils.SAVE_BUTTON_GOOGLE)

        try:
            save_button_disappeared = wait_vanish(Utils.SAVE_BUTTON_GOOGLE, Settings.FIREFOX_TIMEOUT)
            assert_true(self, save_button_disappeared, 'Google main page is displayed')
        except FindError:
            raise FindError('\'Save\' google button is still available.')

        navigate(LocalWeb.FIREFOX_TEST_SITE)

        top_two_thirds_of_screen = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)

        firefox_site_loaded = exists(LocalWeb.FIREFOX_LOGO, Settings.FIREFOX_TIMEOUT)
        assert_true(self, firefox_site_loaded, 'Page successfully loaded, firefox logo found.')

        select_location_bar()
        paste('moz')

        mozilla_search_one_offs_available = exists(moz_pattern, Settings.FIREFOX_TIMEOUT, top_two_thirds_of_screen)
        assert_true(self, mozilla_search_one_offs_available, 'Searched string found at the bottom of the drop-down '
                                                             'list.')

        search_settings_button = exists(search_settings_pattern, Settings.FIREFOX_TIMEOUT, top_two_thirds_of_screen)
        assert_true(self, search_settings_button, 'The \'Search settings\' button is displayed in the awesome bar.')

        type(Key.UP)
        key_to_one_off_search(twitter_one_off_button_highlight_pattern)

        twitter_one_off_highlight = exists(twitter_one_off_button_highlight_pattern, Settings.FIREFOX_TIMEOUT,
                                           top_two_thirds_of_screen)
        assert_true(self, twitter_one_off_highlight, 'The \'Twitter\' one-off button is highlighted.')

        type(Key.ENTER)

        new_tab_twitter_search_results = exists(new_tab_twitter_search_results_pattern, Settings.FIREFOX_TIMEOUT) \
            or exists(new_tab_twitter_search_results_2_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, new_tab_twitter_search_results, 'Twitter search results are opened in the same tab.')

        new_tab()

        select_location_bar()
        paste('test')

        google_on_off_button_private_window = exists(google_on_off_private_window_pattern, Settings.FIREFOX_TIMEOUT,
                                                     top_two_thirds_of_screen)
        assert_true(self, google_on_off_button_private_window, 'The\'Google\' one-off button found.')

        click(google_on_off_private_window_pattern)

        magnifying_glass = exists(magnifying_glass_pattern, Settings.SITE_LOAD_TIMEOUT, top_two_thirds_of_screen)
        assert_true(self, magnifying_glass, 'Page successfully loaded using the \'Google\' engine.')

        test_item = exists(test_pattern, Settings.SITE_LOAD_TIMEOUT, top_two_thirds_of_screen)
        assert_true(self, test_item, 'Searched item is successfully found in the page opened by the \'Google\' search '
                                     'engine.')

        close_window()
