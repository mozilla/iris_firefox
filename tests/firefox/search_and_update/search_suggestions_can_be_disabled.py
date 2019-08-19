# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Search suggestions can be disabled.',
        locale=['en-US'],
        test_case_id='4273',
        test_suite_id='83',
    )
    def run(self, firefox):
        provide_search_suggestions_pattern = Pattern('provide_search_suggestions.png')
        show_suggestions_pattern = Pattern('show_suggestions.png')
        google_logo_content_search_field_pattern = Pattern('google_logo_content_search_field.png')
        search_suggestions_not_displayed_search_bar_pattern = Pattern('search_suggestions_are_disabled_search_bar.png')
        search_suggestions_not_displayed_content_search_pattern = \
            Pattern('search_suggestions_are_disabled_content_search.png')

        # Enable the search bar.
        change_preference('browser.search.widget.inNavBar', True)

        search_bar_enabled = exists(LocationBar.SEARCH_BAR_MAGNIFYING_GLASS, FirefoxSettings.FIREFOX_TIMEOUT)
        assert search_bar_enabled is True, 'The search bar is successfully enabled.'

        right_click(LocationBar.SEARCH_BAR_MAGNIFYING_GLASS)

        show_suggestions_available = exists(show_suggestions_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert show_suggestions_available is True, 'The \'Show Suggestions\' option is visible.'

        # Uncheck the 'Show Suggestions' option.
        click(show_suggestions_pattern, Settings.DEFAULT_UI_DELAY)

        # Go to 'about:preferences#search' and check that the the 'Provide search suggestions' option is unchecked.
        navigate('about:preferences#search')

        provide_search_suggestions = exists(provide_search_suggestions_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert provide_search_suggestions is True, 'The \'Provide search suggestions\' option is disabled.'

        # Type in some random text in the Search Bar and content search field.
        new_tab()

        select_search_bar()

        paste('test')

        suggestions_search_not_displayed = exists(search_suggestions_not_displayed_search_bar_pattern,
                                                  FirefoxSettings.FIREFOX_TIMEOUT)
        assert suggestions_search_not_displayed is True, 'Search suggestions are not displayed for any of these' \
                                                         ' locations.'

        google_logo_search_field = exists(google_logo_content_search_field_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert google_logo_search_field is True, 'Google logo from content search field found.'

        click(google_logo_content_search_field_pattern)

        paste('test')

        suggestions_content_not_displayed = exists(search_suggestions_not_displayed_content_search_pattern,
                                                   FirefoxSettings.FIREFOX_TIMEOUT)
        assert suggestions_content_not_displayed is True, 'Search suggestions are not shown for the input in question.'

        # Go to 'about:preferences#search' and check the 'Provide search suggestions' option.
        navigate('about:preferences#search')

        provide_search_suggestions = exists(provide_search_suggestions_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert provide_search_suggestions is True, 'The \'Provide search suggestions\' option is disabled.'

        click(provide_search_suggestions_pattern)

        # Type in some random text in the Search Bar and content search field.
        new_tab()

        select_search_bar()

        paste('test')

        suggestions_search_displayed = exists(search_suggestions_not_displayed_search_bar_pattern,
                                              FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert suggestions_search_displayed is False, 'Search suggestions are shown for the input in question.'

        google_logo_search_field = exists(google_logo_content_search_field_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert google_logo_search_field is True, 'Google logo from content search field found.'

        click(google_logo_content_search_field_pattern)

        paste('test')

        suggestions_content_displayed = exists(search_suggestions_not_displayed_content_search_pattern,
                                               FirefoxSettings.FIREFOX_TIMEOUT)
        assert suggestions_content_displayed is False, 'Search suggestions are shown for the input in question.'
