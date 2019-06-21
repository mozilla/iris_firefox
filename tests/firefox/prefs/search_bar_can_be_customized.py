# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='The default search engine can be successfully customized',
        test_case_id='143591',
        test_suite_id='2241',
        locale=['en-US'],
    )
    def run(self, firefox):
        preferences_search_pattern = AboutPreferences.ABOUT_PREFERENCE_SEARCH_PAGE_PATTERN
        # add_search_bar_in_toolbar_deselected_pattern = Pattern('add_search_bar_in_toolbar_deselected.png')
        # add_search_bar_in_toolbar_selected_pattern = Pattern('add_search_bar_in_toolbar_selected.png')
        default_search_engine_google_pattern = Pattern('default_search_engine_google.png')
        amazon_search_engine_pattern = Pattern('amazon_search_engine.png')

        navigate('about:preferences#search')

        preferences_search_loaded = exists(preferences_search_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert preferences_search_loaded, 'The about:preferences page is successfully loaded.'

        url_bar_location = find(preferences_search_pattern)
        url_bar_height = preferences_search_pattern.get_size()[1]
        test_search_region = Region(0, url_bar_location.y + url_bar_height,
                                    Screen.SCREEN_WIDTH // 3, Screen.SCREEN_HEIGHT // 3)

        default_search_engine_google = exists(default_search_engine_google_pattern)
        assert default_search_engine_google, '"Default Search Engine" option available.'

        click(default_search_engine_google_pattern, 1)

        amazon_search_engine = exists(amazon_search_engine_pattern)
        assert amazon_search_engine, 'A different default search engine available.'

        click(amazon_search_engine_pattern, 1)

        new_tab()

        navigate('about:newtab')
        select_search_bar()

        paste('test search')

        type(Key.ENTER)

        search_is_done = exists('test search', FirefoxSettings.FIREFOX_TIMEOUT * 2, region=test_search_region)
        assert search_is_done, 'The search is made successfully.'

        select_location_bar()

        edit_copy()

        search_engine_changed = 'amazon.com' in get_clipboard()

        assert search_engine_changed, 'The search is made by the selected search engine.'
