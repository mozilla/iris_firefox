# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Firefox hijacking'
        self.test_case_id = '217858'
        self.test_suite_id = '3063'
        self.locales = ['en-US']

    def run(self):
        about_preferences_search_pattern = Pattern('about_preferences_search.png')
        about_preferences_home_pattern = Pattern('about_preferences_home.png')
        default_search_engine_pattern = Pattern('default_search_engine.png')
        firefox_home_default_pattern = Pattern('firefox_home_default.png')
        search_suggestions_default_pattern = Pattern('search_suggestions_default.png')
        search_result_default_pattern = Pattern('search_result_default.png')
        top_sites_pattern = Pattern('top_sites.png')

        navigate('about:preferences#search')

        about_preferences_search_opened = exists(about_preferences_search_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, about_preferences_search_opened, 'About preferences search page is successfully opened')

        search_engine_is_default = exists(default_search_engine_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, search_engine_is_default, 'The default search engine is not changed')

        navigate('about:preferences#home')

        about_preferences_home_opened = exists(about_preferences_home_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, about_preferences_home_opened, 'About preferences home page is successfully opened')

        firefox_home_is_default = exists(firefox_home_default_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, firefox_home_is_default, 'The default home page is not changed')

        click(NavBar.HOME_BUTTON)

        new_tab_pattern_exists = exists(Tabs.NEW_TAB_HIGHLIGHTED, DEFAULT_FIREFOX_TIMEOUT)
        top_sites_pattern_exists = exists(top_sites_pattern)
        assert_true(self, new_tab_pattern_exists and top_sites_pattern_exists, 'The set homepage is opened')

        paste('text')

        search_suggestions_displays = exists(search_suggestions_default_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, search_suggestions_displays, 'The search suggestions dropdown is displayed, '
                                                       'no extra search engines are added.')

        type(Key.ENTER)

        search_result_is_default = exists(search_result_default_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, search_result_is_default, 'Search results displayed, with the known/selected search-engine.')
