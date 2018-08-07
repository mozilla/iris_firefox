# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This test case perform one-offs searches in private browsing.'

    def run(self):
        moz = 'moz.png'
        url = LocalWeb.FIREFOX_TEST_SITE
        search_settings = 'search_settings.png'
        twitter_one_off_button_highlight = 'twitter_one_off_button_highlight.png'
        new_tab_twitter_search_results = 'new_tab_twitter_search_results.png'
        google_on_off_button_private_window = 'google_on_off_button_private_window.png'
        magnifying_glass = 'magnifying_glass.png'
        test = 'test.png'

        new_private_window()

        navigate(url)

        region = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        select_location_bar()
        paste('moz')

        expected = region.exists(moz, 10)
        assert_true(self, expected, 'Searched string found at the bottom of the drop-down list.')

        expected = region.exists(search_settings, 10)
        assert_true(self, expected, 'The \'Search settings\' button is displayed in the awesome bar.')

        for i in range(13):
            scroll_down()

        expected = region.exists(twitter_one_off_button_highlight, 10)
        assert_true(self, expected, 'The \'Twitter\' one-off button is highlighted.')

        type(Key.ENTER)
        time.sleep(DEFAULT_UI_DELAY_LONG)

        expected = exists(new_tab_twitter_search_results, 10)
        assert_true(self, expected, 'Twitter search results are opened in the same tab.')

        new_tab()
        time.sleep(DEFAULT_UI_DELAY)

        select_location_bar()
        paste('test')

        expected = region.exists(google_on_off_button_private_window, 10)
        assert_true(self, expected, 'The\'Google\' one-off button found.')

        if Settings.get_os() == Platform.MAC:
            key_down(Key.CMD)
        else:
            key_down(Key.CTRL)

        click(google_on_off_button_private_window)

        if Settings.get_os() == Platform.MAC:
            key_up(Key.CMD)
        else:
            key_up(Key.CTRL)

        # move focus to the new tab opened.
        next_tab()

        expected = region.exists(magnifying_glass, 10)
        assert_true(self, expected, 'Page successfully loaded using the \'Google\' engine.')

        expected = region.exists(test, 10)
        assert_true(self, expected, 'Searched item is successfully found in the page opened by the \'Google\' search '
                                    'engine.')
