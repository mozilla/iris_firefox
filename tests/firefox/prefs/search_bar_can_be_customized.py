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
        default_search_engine_google_pattern = Pattern('default_search_engine_google.png')
        amazon_search_engine_pattern = Pattern('amazon_search_engine.png').similar(0.9)
        search_result_default_pattern = Pattern('search_result_default.png')

        navigate('about:preferences#search')

        default_search_engine_google = exists(default_search_engine_google_pattern)
        assert default_search_engine_google, '"Default Search Engine" option available.'

        default_search_engine_google_location = find(default_search_engine_google_pattern)
        default_search_engine_amazon_region = Region(default_search_engine_google_location.x-10,
                                                     default_search_engine_google_location.y-10,
                                                     Screen.SCREEN_WIDTH // 5, Screen.SCREEN_HEIGHT // 5)

        click(default_search_engine_google_pattern, 1)

        amazon_search_engine = exists(amazon_search_engine_pattern, region=default_search_engine_amazon_region)
        assert amazon_search_engine, 'A different default search engine available.'

        click(amazon_search_engine_pattern, 1, region=default_search_engine_amazon_region)

        new_tab()

        navigate('about:newtab')
        select_search_bar()

        paste('test search')

        type(Key.ENTER)

        assert exists(amazon_search_engine_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT), \
            'Search results displayed, with the known/selected search-engine.'

        test_search_region = Region(0, 0, Screen.SCREEN_WIDTH, Screen.SCREEN_HEIGHT // 2)

        search_is_done = exists('test search', FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT, region=test_search_region)
        assert search_is_done, 'The search is made successfully.'

        select_location_bar()

        edit_copy()

        search_engine_changed = 'amazon.com' in get_clipboard()

        assert search_engine_changed, 'The search is made by the selected search engine.'
