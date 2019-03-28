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
        search_result_default_pattern = Pattern('search_result_default.png')
        top_sites_pattern = Pattern('top_sites.png')
        bing_search_suggestion_pattern = Pattern('bing_search_suggestion.png')
        amazon_search_suggestion_pattern = Pattern('amazon_search_suggestion.png')
        duck_search_suggestion_pattern = Pattern('duck_search_suggestion.png')
        ebay_search_suggestion_pattern = Pattern('ebay_search_suggestion.png')
        google_search_suggestion_pattern = Pattern('google_search_suggestion.png')
        twitter_search_suggestion_pattern = Pattern('twitter_search_suggestion.png')
        wiki_search_suggestion_pattern = Pattern('wiki_search_suggestion.png')

        search_suggestions = [google_search_suggestion_pattern, bing_search_suggestion_pattern,
                              amazon_search_suggestion_pattern, duck_search_suggestion_pattern,
                              ebay_search_suggestion_pattern, twitter_search_suggestion_pattern]

        navigate('about:preferences#search')

        about_preferences_search_opened = exists(about_preferences_search_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, about_preferences_search_opened, 'About preferences search page is successfully opened')

        search_engine_is_default = exists(default_search_engine_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, search_engine_is_default, 'The default search engine is not changed')

        navigate('about:preferences#home')

        about_preferences_home_opened = exists(about_preferences_home_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, about_preferences_home_opened, 'About preferences home page is successfully opened')

        firefox_home_is_default = exists(firefox_home_default_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, firefox_home_is_default, 'The default home page is not changed')

        click(NavBar.HOME_BUTTON)

        new_tab_pattern_exists = exists(Tabs.NEW_TAB_HIGHLIGHTED, Settings.FIREFOX_TIMEOUT)
        top_sites_pattern_exists = exists(top_sites_pattern)
        assert_true(self, new_tab_pattern_exists and top_sites_pattern_exists, 'The set homepage is opened')

        paste('text')

        google_search_suggestion_exists = exists(google_search_suggestion_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, google_search_suggestion_exists, 'Search suggestion drop-down displayed')

        google_search_suggestion_location = find(google_search_suggestion_pattern)
        google_search_suggestion_width, google_search_suggestion_height = google_search_suggestion_pattern.get_size()

        coordinate_x = google_search_suggestion_location.x

        for search_engine in search_suggestions:
            num = search_suggestions.index(search_engine) + 1
            suggestion_region = Region(coordinate_x, google_search_suggestion_location.y,
                                       google_search_suggestion_width, google_search_suggestion_height)

            search_suggestions_displays = exists(search_engine, in_region=suggestion_region)
            assert_true(self, search_suggestions_displays, 'The search suggestions #' + str(num) + ' exists')

            coordinate_x += google_search_suggestion_width

        search_suggestions_displays = exists(wiki_search_suggestion_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, search_suggestions_displays, 'All search suggestions is displayed and no'
                                                       ' extra search engines are added.')

        type(Key.ENTER)

        search_result_is_default = exists(search_result_default_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, search_result_is_default, 'Search results displayed, with the known/selected search-engine.')
