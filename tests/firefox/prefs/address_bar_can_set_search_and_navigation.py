# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='The address bar can be successfully set for search and navigation',
        test_case_id='143590',
        test_suite_id='2241',
        locale=['en-US'],
    )
    def run(self, firefox):
        preferences_search_pattern = AboutPreferences.ABOUT_PREFERENCE_SEARCH_PAGE_PATTERN
        use_address_bar_deselected_pattern = Pattern('use_address_bar_deselected.png')
        use_address_bar_selected_pattern = Pattern('use_address_bar_selected.png')
        search_result_default_pattern = Pattern('search_result_default.png')

        navigate('about:preferences#search')

        preferences_search_loaded = exists(preferences_search_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert preferences_search_loaded, 'The about:preferences page is successfully loaded.'

        url_bar_location = find(preferences_search_pattern)
        url_bar_height = preferences_search_pattern.get_size()[1]
        test_search_region = Region(0, url_bar_location.y + url_bar_height,
                                    Screen.SCREEN_WIDTH // 3, Screen.SCREEN_HEIGHT // 3)

        use_address_bar_deselected = exists(use_address_bar_deselected_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert use_address_bar_deselected, '"Use the address bar for search bar and navigation" is not active.'

        click(use_address_bar_deselected_pattern)

        use_address_bar_selected = exists(use_address_bar_selected_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert use_address_bar_selected, 'The option "Use the address bar for search bar and navigation" is selected ' \
                                         'by default. '

        new_tab()

        select_location_bar()

        paste('test search')

        type(Key.ENTER)

        assert exists(search_result_default_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT), \
            'Search results displayed, with the known/selected search-engine.'

        search_is_done = exists('test search', FirefoxSettings.FIREFOX_TIMEOUT * 2, region=test_search_region)
        assert search_is_done, 'The search is done without any issues. '
