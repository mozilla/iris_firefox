# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Search bar can be successfully added/removed from the toolbar',
        test_case_id='143589',
        test_suite_id='2241',
        locale=['en-US'],
    )
    def run(self, firefox):
        preferences_search_pattern = AboutPreferences.ABOUT_PREFERENCE_SEARCH_PAGE_PATTERN
        add_search_bar_in_toolbar_deselected_pattern = Pattern('add_search_bar_in_toolbar_deselected.png')
        add_search_bar_in_toolbar_selected_pattern = Pattern('add_search_bar_in_toolbar_selected.png')
        search_result_default_pattern = Pattern('search_result_default.png')
        use_address_bar_deselected_pattern = Pattern('use_address_bar_deselected.png')
        use_address_bar_selected_pattern = Pattern('use_address_bar_selected.png')

        navigate('about:preferences#search')

        preferences_search_loaded = exists(preferences_search_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert preferences_search_loaded, 'The about:preferences page is successfully loaded.'

        url_bar_location = find(preferences_search_pattern)
        url_bar_height = preferences_search_pattern.get_size()[1]
        test_search_region = Region(0, url_bar_location.y + url_bar_height,
                                    Screen.SCREEN_WIDTH // 3, Screen.SCREEN_HEIGHT // 3)

        add_search_bar_in_toolbar_deselected = exists(add_search_bar_in_toolbar_deselected_pattern,
                                                      FirefoxSettings.FIREFOX_TIMEOUT)
        assert add_search_bar_in_toolbar_deselected, 'Option "Add search bar in toolbar" is deselected.'

        click(add_search_bar_in_toolbar_deselected_pattern, 1)

        add_search_bar_in_toolbar_selected = exists(add_search_bar_in_toolbar_selected_pattern,
                                                    FirefoxSettings.FIREFOX_TIMEOUT)
        assert add_search_bar_in_toolbar_selected, 'The option "Add search bar in toolbar" is successfully selected.'

        new_tab()

        select_search_bar()

        paste('test search')

        type(Key.ENTER)

        assert exists(search_result_default_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT), \
            'Search results displayed, with the known/selected search-engine.'

        search_is_done = exists('test search', FirefoxSettings.FIREFOX_TIMEOUT * 2, region=test_search_region)
        assert search_is_done, 'The search is done without any issues. '

        navigate('about:preferences#search')

        preferences_search_loaded = exists(preferences_search_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert preferences_search_loaded, 'The about:preferences page is successfully loaded.'

        use_address_bar_deselected = exists(use_address_bar_deselected_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert use_address_bar_deselected, 'Option "Use the address bar for search and navigation" is available'

        click(use_address_bar_deselected_pattern, 1)

        use_address_bar_selected = exists(use_address_bar_selected_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert use_address_bar_selected, 'Option "Use the address bar for search and navigation" selected'

        try:
            search_bar_removed = wait_vanish(LocationBar.SEARCH_BAR.similar(0.95), region=Screen.UPPER_RIGHT_CORNER)
        except FindError:
            raise FindError('Search bar is not removed')

        assert search_bar_removed, 'The search bar is removed from the right side of the address bar.'
