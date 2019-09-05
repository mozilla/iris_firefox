# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This test case perform a search by keyboard only.',
        locale=['en-US'],
        test_case_id='108268',
        test_suite_id='1902',
        profile_preferences={'browser.contentblocking.enabled': False}
    )
    def run(self, firefox):
        this_time_search_with_pattern = Pattern('this_time_search_with.png')
        twitter_search_results_localhost = Pattern('twitter_search_results_localhost.png')
        twitter_search_results_localhost_2 = Pattern('twitter_search_results_localhost_2.png')
        twitter_one_off_button_highlight_pattern = Pattern('twitter_one_off_button_highlight.png').similar(.99)
        bing_one_off_button_highlight_pattern = Pattern('bing_one_off_button_highlight.png').similar(.99)
        bing_search_results_pattern = Pattern('bing_search_results_localhost.png')
        duck_one_off_button_highlight_pattern = Pattern('duck_one_off_button_highlight.png')
        duck_go_search_result_pattern = Pattern('duck_go_search_resul.png')


        region = Screen().new_region(0, 0, Screen.SCREEN_WIDTH, 2 * Screen.SCREEN_HEIGHT / 3)

        select_location_bar()
        paste('127')

        one_off_bar_displayed = exists(this_time_search_with_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert one_off_bar_displayed, 'The one-off bar is displayed at the bottom of awesomebar drop-down'

        assert scroll_until_pattern_found(twitter_one_off_button_highlight_pattern, type, (Key.UP,), 20, 1),\
            'The \'Search settings\' button is highlighted.'

        type(Key.ENTER)

        twitter_search_results_localhost_exists = exists(twitter_search_results_localhost,
                                                         FirefoxSettings.SHORT_FIREFOX_TIMEOUT) or \
                                                  exists(twitter_search_results_localhost_2,
                                                         FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert twitter_search_results_localhost_exists, 'A new tab with \'Twitter\' search results' \
                                                        ' for the searched string is opened.'

        select_location_bar()
        paste('127.0')

        one_off_bar_displayed = exists(this_time_search_with_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert one_off_bar_displayed, 'The one-off bar is displayed at the bottom of awesomebar drop-down'

        assert scroll_until_pattern_found(bing_one_off_button_highlight_pattern, type, (Key.UP,), 20, 1),\
            'The \'Search settings\' button is highlighted.'

        type(Key.ENTER)

        bing_search_results_localhost_exists = exists(bing_search_results_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bing_search_results_localhost_exists, '\'Bing\' search results are opened in the same tab.'

        select_location_bar()
        paste('127.0')

        one_off_bar_displayed = exists(this_time_search_with_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert one_off_bar_displayed, 'The one-off bar is displayed at the bottom of awesomebar drop-down'

        assert scroll_until_pattern_found(duck_one_off_button_highlight_pattern, type, (Key.UP,), 20, 1),\
            'The \'Search settings\' button is highlighted.'

        type(Key.ENTER)

        bing_search_results_localhost_exists = exists(duck_go_search_result_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bing_search_results_localhost_exists, '\'Duck-duck-go\' search results are opened in the same tab.'

