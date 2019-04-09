# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Search suggestions can be disabled.'
        self.test_case_id = '4273'
        self.test_suite_id = '83'
        self.locale = ['en-US']

    def run(self):
        search_bar_pattern = Pattern('search_bar.png')
        provide_search_suggestions_pattern = Pattern('provide_search_suggestions.png')
        show_suggestions_pattern = Pattern('show_suggestions.png')
        google_logo_content_search_field_pattern = Pattern('google_logo_content_search_field.png')
        search_suggestions_not_displayed_search_bar_pattern = Pattern('search_suggestions_are_disabled_search_bar.png')
        search_suggestions_not_displayed_content_search_pattern = \
            Pattern('search_suggestions_are_disabled_content_search.png')

        # Enable the search bar.
        change_preference('browser.search.widget.inNavBar', True)

        search_bar_enabled = exists(search_bar_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, search_bar_enabled, 'The search bar is successfully enabled.')

        right_click(search_bar_pattern)

        show_suggestions_available = exists(show_suggestions_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, show_suggestions_available, 'The \'Show Suggestions\' option is visible.')

        # Uncheck the 'Show Suggestions' option.
        click(show_suggestions_pattern, Settings.TINY_FIREFOX_TIMEOUT)

        # Go to 'about:preferences#search' and check that the the 'Provide search suggestions' option is unchecked.
        navigate('about:preferences#search')

        provide_search_suggestions = exists(provide_search_suggestions_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, provide_search_suggestions, 'The \'Provide search suggestions\' option is disabled.')

        # Type in some random text in the Search Bar and content search field.
        new_tab()

        select_search_bar()

        paste('test')

        suggestions_search_not_displayed = exists(search_suggestions_not_displayed_search_bar_pattern,
                                                  Settings.FIREFOX_TIMEOUT)
        assert_true(self, suggestions_search_not_displayed, 'Search suggestions are not displayed for any of these'
                                                            ' locations.')

        google_logo_search_field = exists(google_logo_content_search_field_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, google_logo_search_field, 'Google logo from content search field found.')

        click(google_logo_content_search_field_pattern)

        paste('test')

        suggestions_content_not_displayed = exists(search_suggestions_not_displayed_content_search_pattern,
                                                   Settings.FIREFOX_TIMEOUT)
        assert_true(self, suggestions_content_not_displayed, 'Search suggestions are not shown for the input '
                                                             'in question.')

        # Go to 'about:preferences#search' and check the 'Provide search suggestions' option.
        navigate('about:preferences#search')

        provide_search_suggestions = exists(provide_search_suggestions_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, provide_search_suggestions, 'The \'Provide search suggestions\' option is disabled.')

        click(provide_search_suggestions_pattern)

        # Type in some random text in the Search Bar and content search field.
        new_tab()

        select_search_bar()

        paste('test')

        suggestions_search_displayed = exists(search_suggestions_not_displayed_search_bar_pattern,
                                              Settings.SITE_LOAD_TIMEOUT)
        assert_false(self, suggestions_search_displayed, 'Search suggestions are shown for the input in question.')

        google_logo_search_field = exists(google_logo_content_search_field_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, google_logo_search_field, 'Google logo from content search field found.')

        click(google_logo_content_search_field_pattern)

        paste('test')

        suggestions_content_displayed = exists(search_suggestions_not_displayed_content_search_pattern,
                                               Settings.FIREFOX_TIMEOUT)
        assert_false(self, suggestions_content_displayed, 'Search suggestions are shown for the input in question.')
