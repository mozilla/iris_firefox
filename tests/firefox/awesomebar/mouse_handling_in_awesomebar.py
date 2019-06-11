# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Mouse handling - in the awesomebar.',
        locale=['en-US'],
        test_case_id='108282',
        test_suite_id='1902'
    )
    def run(self, firefox):
        twitter_one_off_button_highlight_pattern = Pattern('twitter_one_off_button_highlight.png')
        google_one_off_button_pattern = Pattern('google_one_off_button.png')
        search_with_google_one_off_string_pattern = Pattern('search_with_Google_one_off_string.png')
        search_suggestion_opened_tab_pattern = Pattern('search_suggestion_opened_tab.png').similar(.7)

        navigate(LocalWeb.FIREFOX_TEST_SITE)

        expected = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Firefox page loaded successfully.'

        select_location_bar()
        paste('127')

        # Press "Alt" and arrow up keys to select an one-off button and hover over it.
        repeat_key_up(3)

        expected = exists(twitter_one_off_button_highlight_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'The \'Twitter\' one-off button is highlighted.'

        hover(twitter_one_off_button_highlight_pattern)

        expected = exists(twitter_one_off_button_highlight_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'The \'Twitter\' one-off button is still highlighted in the previous color.'

        # Without closing the autocomplete drop-down, move mouse over an one-off button.
        expected = exists(google_one_off_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'The \'Google\' one-off button found.'

        hover(google_one_off_button_pattern)

        expected = exists(search_with_google_one_off_string_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Successfully hovered over the \'Google\' one off.'

        # Hover over an autocomplete result that is not selected and click on it.
        expected = exists(search_suggestion_opened_tab_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Opened tab found between the search suggestions.'

        click(search_suggestion_opened_tab_pattern)

        expected = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Clicking a result that is not the selected loads the clicked result, not the selected result.'
