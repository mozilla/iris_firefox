# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This test case disables the web search in the awesomebar.',
        locale=['en-US'],
        test_case_id='108254',
        test_suite_id='1902',
        preferences={'browser.contentblocking.enabled': False}
    )
    def run(self, firefox):
        page_bookmarked_pattern = Bookmarks.StarDialog.NEW_BOOKMARK
        google_one_off_button_pattern = Pattern('google_one_off_button.png')
        google_search_results_pattern = Pattern('google_search_results.png')
        search_suggestion_bookmarked_tab_pattern = Pattern('search_suggestion_bookmarked_tab.png').similar(.6)
        search_suggestion_opened_tab_pattern = Pattern('search_suggestion_opened_tab.png').similar(.6)
        search_suggestion_history_pattern = Pattern('search_suggestion_history.png').similar(.6)
        popular_search_suggestion_pattern = Pattern('popular_search_suggestion.png')
        mozilla_tab_logo_pattern = Pattern('mozilla_tab_logo.png')

        top_two_thirds_region = Region(0, 0, Screen.SCREEN_WIDTH, 2 * Screen.SCREEN_HEIGHT / 3)
        autofill_navigated = False

        # Make some browsing history to check it later in awesome bar
        new_tab()
        navigate('mozilla.org')

        mozilla_page_opened = exists(mozilla_tab_logo_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert mozilla_page_opened, 'Mozilla page opened'

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        expected = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.FIREFOX_TIMEOUT, region=top_two_thirds_region)
        assert expected, 'Mozilla page loaded successfully.'

        bookmark_page()

        expected = exists(page_bookmarked_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=top_two_thirds_region)
        assert expected, 'Page was bookmarked.'

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)

        expected = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT, region=top_two_thirds_region)
        assert expected, 'Firefox page loaded successfully.'

        new_tab()
        navigate(LocalWeb.FOCUS_TEST_SITE)

        expected = exists(LocalWeb.FOCUS_LOGO, FirefoxSettings.FIREFOX_TIMEOUT, region=top_two_thirds_region)
        assert expected, 'Focus page loaded successfully.'

        # 2. Enter a search term in the URL bar, hover any one-off button and left click on it.
        new_tab()

        # The autocomplete drop-down with matching results for: bookmarks, open tabs, history, suggestions is displayed.
        select_location_bar()
        paste('m')

        expected = exists(search_suggestion_bookmarked_tab_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                          region=top_two_thirds_region)
        assert expected, 'Bookmarked page found between search suggestions.'

        select_location_bar()
        paste('ox')

        expected = exists(search_suggestion_opened_tab_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                          region=top_two_thirds_region)
        assert expected, 'Opened tab found between search suggestions.'

        select_location_bar()
        paste('f')

        expected = exists(search_suggestion_history_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                          region=top_two_thirds_region)
        assert expected, 'Web pages from personal browsing history found between search suggestions.'

        expected = exists(popular_search_suggestion_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                          region=top_two_thirds_region)
        assert expected, 'Popular search suggestions from the default search engine found between search suggestions.'

        # 2. Enter a search term in the URL bar, hover any one-off button and left click on it.

        select_location_bar()
        type('moz')

        time.sleep(Settings.DEFAULT_UI_DELAY)

        one_off_button_exists = exists(google_one_off_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                                       region=top_two_thirds_region)
        assert one_off_button_exists, 'The \'Google\' one-off button found.'

        google_one_off_button_location = find(google_one_off_button_pattern, Screen.LEFT_THIRD)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        click(google_one_off_button_location, 1)

        # - Firefox takes you to search results using the search provider of the selected one-off button

        search_results_available = exists(google_search_results_pattern.similar(0.7), FirefoxSettings.FIREFOX_TIMEOUT,
                                          region=Screen.TOP_THIRD)
        assert search_results_available, 'Google search results are displayed.'

        close_tab()

        # 3. Go to about:config and set the preference keyword.enabled to false.
        change_preference('keyword.enabled', 'false')

        # 4. Enter a search in the URL bar and hit enter.
        new_tab()

        select_location_bar()
        type('inputstring')

        time.sleep(Settings.DEFAULT_UI_DELAY)

        type(Key.ENTER)

        # The search is executed with URL autocomplete.

        for page_not_found_rendered in range(3):
            select_location_bar()

            edit_select_all()

            edit_copy()

            url_text = get_clipboard()

            autofill_navigated = 'http://www.inputstring.com/' in url_text
            if autofill_navigated:
                break

            time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        assert 'http://www.inputstring.com/' in url_text, 'The search is executed with URL autocomplete.'

        # 5. Perform a search in the URL bar using the same one-off button as in step 2.
        # The search is executed on using selected engine.

        new_tab()
        select_location_bar()
        type('moz')

        time.sleep(Settings.DEFAULT_UI_DELAY)

        one_off_button_exists = exists(google_one_off_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                                       )
        assert one_off_button_exists, 'The \'Google\' one-off button found.'

        click(google_one_off_button_location, 1)

        # The search is executed on using selected engine.
        # Firefox takes you to search results using the search provider of the selected one-off button

        search_results_available = exists(google_search_results_pattern.similar(0.7), FirefoxSettings.FIREFOX_TIMEOUT,
                                          )
        assert search_results_available, 'Google search results are displayed. The search is executed on using ' \
                                         'selected engine.'
