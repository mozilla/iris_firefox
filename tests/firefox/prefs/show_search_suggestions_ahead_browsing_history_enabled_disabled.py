# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='The "Show search suggestions ahead of browsing history in address bar results" can be '
                    'successfully enabled/disabled',
        test_case_id='143594',
        test_suite_id='2241',
        locale=['en-US'],
    )
    def run(self, firefox):
        preferences_search_page = AboutPreferences.ABOUT_PREFERENCE_SEARCH_PAGE_PATTERN
        suggestions_displayed_pattern = Pattern('suggestions_displayed.png')
        browsing_history_search_bar_pattern = Pattern('browsing_history_search_bar.png')
        provide_search_suggestions_pattern = Pattern('provide_search_suggestions_checked.png')
        show_search_suggestions_pattern = Pattern('show_search_suggestions_checked.png')
        show_search_browsing_history_checked_pattern = Pattern('show_search_browsing_history_checked.png')
        show_search_browsing_history_unchecked_pattern = Pattern('show_search_browsing_history_unchecked.png')

        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        assert exists(LocalWeb.MOZILLA_LOGO), 'Mozilla site loaded.'

        close_tab()

        new_tab()
        navigate(LocalWeb.FOCUS_TEST_SITE)

        assert exists(LocalWeb.FOCUS_LOGO), 'Focus site loaded.'

        close_tab()

        navigate('about:preferences#search')

        preferences_privacy_page = exists(preferences_search_page, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert preferences_privacy_page, 'The about:preferences#privacy page is successfully loaded.'

        # From "Default Search Engine" make sure that the options "Provide search suggestions",
        # "Show search suggestions in address bar results" and
        # "Show search suggestions ahead of browsing history in address bar results" are selected.

        assert find_in_region_from_pattern(provide_search_suggestions_pattern, AboutPreferences.CHECKED_BOX) and \
            find_in_region_from_pattern(show_search_suggestions_pattern, AboutPreferences.CHECKED_BOX) and \
            find_in_region_from_pattern(show_search_browsing_history_checked_pattern, AboutPreferences.CHECKED_BOX), \
            'The options "Provide search suggestions", "Show search suggestions in address bar results" and ' \
            '"Show search suggestions ahead of browsing history in address bar results" are selected.'

        new_tab()

        select_location_bar()

        paste('2000 ')

        # The suggestions are displayed for any of the available search engines.
        suggestions_displayed = exists(suggestions_displayed_pattern, FirefoxSettings.FIREFOX_TIMEOUT)

        # Underneath those the browsing history is displayed.
        browsing_history_search_bar = exists(browsing_history_search_bar_pattern, FirefoxSettings.FIREFOX_TIMEOUT)

        assert suggestions_displayed and browsing_history_search_bar, \
            'Suggestions and browsing history displayed after search'

        close_tab()

        assert find_in_region_from_pattern(show_search_browsing_history_checked_pattern, AboutPreferences.CHECKED_BOX),\
            'Privacy options successfully opened.'

        click(show_search_browsing_history_checked_pattern, 1)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)  # wait for proper pattern

        # The option "Show search suggestions ahead of browsing history in address bar results" is unchecked.
        assert find_in_region_from_pattern(show_search_browsing_history_unchecked_pattern,
                                           AboutPreferences.UNCHECKED_BOX), \
            '"Show suggestions ahead of browsing history..." is unchecked.'

        new_tab()

        paste('2000 ')

        exists(suggestions_displayed_pattern, FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        suggestions_displayed_y = find(suggestions_displayed_pattern).y

        exists(browsing_history_search_bar_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        browsing_history_search_bar_y = find(browsing_history_search_bar_pattern).y

        # The browsing history is displayed before the search suggestions.
        assert browsing_history_search_bar_y < suggestions_displayed_y, \
            'The suggestions are no longer displayed for any of the available search engines. Only the browsing' \
            ' history is displayed. '
