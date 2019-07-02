# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Search suggestions can be successfully enabled/disabled',
        test_case_id='143592',
        test_suite_id='2241',
        locale=['en-US'],
    )
    def run(self, firefox):
        google_logo_content_search_field_pattern = Pattern('google_logo_content_search_field.png')
        provide_search_suggestions_checked_pattern = Pattern('provide_search_suggestions_checked.png')
        provide_search_suggestions_unchecked_pattern = Pattern('provide_search_suggestions_unchecked.png')
        test_suggestions_pattern = Pattern('test_suggestions.png')

        # From "Default Search Engine" make sure that the option "Provide search suggestions" is selected.
        navigate('about:preferences#search')

        provide_search_suggestions = exists(provide_search_suggestions_checked_pattern,
                                            FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert provide_search_suggestions is True, 'The \'Provide search suggestions\' option is disabled.'

        new_tab()

        navigate('about:newtab')

        google_search_field = exists(google_logo_content_search_field_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert google_search_field, 'Google search default field is available'

        google_search_field_location = find(google_logo_content_search_field_pattern)

        click(google_search_field_location.offset(100, 5))  # click on the search field

        paste('test ')

        test_suggestions = exists(test_suggestions_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert test_suggestions, 'While typing there are a lot of suggestions displayed in the dropdown.'

        close_tab()

        # Uncheck the box for "Provide search suggestions" option.
        click(provide_search_suggestions_checked_pattern, 1)

        provide_search_suggestions_unchecked = exists(provide_search_suggestions_unchecked_pattern,
                                                      FirefoxSettings.FIREFOX_TIMEOUT)
        assert provide_search_suggestions_unchecked, 'The "Provide search suggestions" option is unchecked.'

        new_tab()

        navigate('about:newtab')

        google_search_field = exists(google_logo_content_search_field_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert google_search_field, 'Google search default field is available'

        click(google_search_field_location.offset(100, 5))  # click on the search field

        paste('test ')

        test_suggestions = exists(test_suggestions_pattern, FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        assert test_suggestions is False, 'While you are typing there aren\'t any suggestions displayed in ' \
                                          'the dropdown for any of the available search engines.'
