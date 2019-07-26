# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This test case checks the awesomebar search after user input.',
        locale=['en-US'],
        test_case_id='108255',
        test_suite_id='1902'
    )
    def run(self, firefox):
        url = LocalWeb.FIREFOX_TEST_SITE
        localhost = Pattern('localhost.png')
        localhost_2 = Pattern('localhost_2.png')
        twitter_one_off_button = Pattern('twitter_one_off_button.png')
        bing_one_off_button = Pattern('bing_one_off_button.png')
        search_in_new_tab = Pattern('search_in_new_tab.png')
        bing_search_results_localhost = Pattern('bing_search_results_localhost.png')
        twitter_search_results_localhost = Pattern('twitter_search_results_localhost.png')
        twitter_search_results_localhost_2 = Pattern('twitter_search_results_localhost_2.png')

        navigate(url)

        firefox_logo_exists = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert firefox_logo_exists, 'Page successfully loaded, firefox logo found.'

        # Type a partial part of the above address and perform a search, in a new tab, using an one-off.
        select_location_bar()
        paste('127')

        localhost_string_exists = exists(localhost, FirefoxSettings.FIREFOX_TIMEOUT)
        assert localhost_string_exists, 'Searched string found at the bottom of the drop-down list.'

        twitter_one_off_button_exists = exists(twitter_one_off_button, FirefoxSettings.FIREFOX_TIMEOUT)
        assert twitter_one_off_button_exists, 'The \'Twitter\' one-off button found.'

        hover(twitter_one_off_button)

        try:
            localhost_string_vanished = wait_vanish(localhost, FirefoxSettings.FIREFOX_TIMEOUT)
            assert localhost_string_vanished, 'The \'Twitter\' one-off button is highlighted.'
        except FindError:
            raise FindError('The \'Twitter\' one-off button is not highlighted.')

        right_click(twitter_one_off_button)

        search_in_new_tab_exists = exists(search_in_new_tab, FirefoxSettings.FIREFOX_TIMEOUT)
        assert search_in_new_tab_exists, 'The \'Search in New Tab\' option found.'

        click(search_in_new_tab)
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        # Move focus to the new tab opened.
        next_tab()
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        close_content_blocking_pop_up()

        twitter_search_results_localhost_exists = exists(twitter_search_results_localhost,
                                                         FirefoxSettings.SHORT_FIREFOX_TIMEOUT) or \
                                                  exists(twitter_search_results_localhost_2,
                                                         FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert twitter_search_results_localhost_exists, 'A new tab with \'Twitter\' search results' \
                                                        ' for the searched string is opened.'

        # Type a partial part of the above address and perform a search, in the same tab, using an one-off .
        select_location_bar()
        paste('127.0')

        localhost_string_exists = exists(localhost_2, FirefoxSettings.FIREFOX_TIMEOUT)
        assert localhost_string_exists, 'Searched string found at the bottom of the drop-down list.'

        bing_one_off_button_exists = exists(bing_one_off_button, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bing_one_off_button_exists, '\'Bing\' one-off button not found.'

        hover(bing_one_off_button)

        try:
            localhost_string_vanished = wait_vanish(localhost, FirefoxSettings.FIREFOX_TIMEOUT)
            assert localhost_string_vanished, 'The \'Bing\' one-off button is highlighted.'
        except FindError:
            raise FindError('The \'Bing\' one-off button is not highlighted.')

        click(bing_one_off_button)
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        bing_search_results_localhost_exists = exists(bing_search_results_localhost,
                                                      FirefoxSettings.FIREFOX_TIMEOUT)
        assert bing_search_results_localhost_exists, '\'Bing\' search results are opened in the same tab.'
