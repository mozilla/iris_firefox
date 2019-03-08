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
        search_suggestions_are_disabled_content_search_pattern = Pattern(
            'search_suggestions_are_disabled_content_search.png')
        search_suggestions_are_disabled_search_bar_pattern = Pattern('search_suggestions_are_disabled_search_bar.png')

        # Enable the search bar.
        change_preference('browser.search.widget.inNavBar', True)

        expected = exists(search_bar_pattern, 10)
        assert_true(self, expected, 'The search bar is successfully enabled.')

        right_click(search_bar_pattern)

        expected = exists(show_suggestions_pattern, 10)
        assert_true(self, expected, 'The \'Show Suggestions\' option is visible.')

        # Uncheck the 'Show Suggestions' option.
        click(show_suggestions_pattern)

        # Go to 'about:preferences#search' and check that the the 'Provide search suggestions' option is unchecked.
        navigate('about:preferences#search')

        expected = exists(provide_search_suggestions_pattern.similar(0.9), 10)
        assert_true(self, expected, 'The \'Provide search suggestions\' option is disabled.')

        # Type in some random text in the Search Bar and content search field.
        select_search_bar()
        paste('test')
        expected = exists(search_suggestions_are_disabled_search_bar_pattern, 10)
        assert_true(self, expected, 'Search suggestions are not shown for the input in question.')

        new_tab()
        expected = exists(google_logo_content_search_field_pattern, 10)
        assert_true(self, expected, 'Google logo from content search field found.')
        click(google_logo_content_search_field_pattern)
        paste('test')
        expected = exists(search_suggestions_are_disabled_content_search_pattern, 10)
        assert_true(self, expected, 'Search suggestions are not shown for the input in question.')

        # Go to 'about:preferences#search' and check the 'Provide search suggestions' option.
        navigate('about:preferences#search')

        click(provide_search_suggestions_pattern)

        # Type in some random text in the Search Bar and content search field.
        select_search_bar()
        paste('test')
        expected = exists(search_suggestions_are_disabled_search_bar_pattern, 10)
        assert_false(self, expected, 'Search suggestions are shown for the input in question.')

        new_tab()
        expected = exists(google_logo_content_search_field_pattern, 10)
        assert_true(self, expected, 'Google logo from content search field found.')
        click(google_logo_content_search_field_pattern)
        paste('test')
        expected = exists(search_suggestions_are_disabled_content_search_pattern, 10)
        assert_false(self, expected, 'Search suggestions are shown for the input in question.')
