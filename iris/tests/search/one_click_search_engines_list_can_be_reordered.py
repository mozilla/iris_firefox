# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'The list of one-click search engines can be reordered.'
        self.test_case_id = '4277'
        self.test_suite_id = '83'
        self.locale = ['en-US']

    def run(self):
        change_search_settings_pattern = Pattern('change_search_settings.png')
        about_preferences_search_page_pattern = Pattern('about_preferences_search_page.png')
        amazon_search_bar_pattern = Pattern('amazon_search_bar.png')
        bing_search_bar_pattern = Pattern('bing_search_bar.png')
        search_engine_pattern = Pattern('search_engine.png')
        amazon_bing_pattern = Pattern('amazon_bing.png')
        amazon_bing_location_bar_pattern = Pattern('amazon_bing_location_bar.png')
        amazon_bing_content_search_pattern = Pattern('amazon_bing_content_search.png')
        google_logo_content_search_field_pattern = Pattern('google_logo_content_search_field.png')
        amazon_bing_search_bar_pattern = Pattern('amazon_bing_search_bar.png').similar(0.6)

        # Enable the search bar.
        change_preference('browser.search.widget.inNavBar', True)

        select_search_bar()
        type(Key.DOWN)

        expected = exists(change_search_settings_pattern, 10)
        assert_true(self, expected, 'The \'Change Search Settings\' button found in the page.')

        click(change_search_settings_pattern)

        expected = exists(about_preferences_search_page_pattern, 10)
        assert_true(self, expected, 'The \'about:preferences#search\' page opened.')

        # Select a search engine from the One-click search engines list and and move its position up in the list via
        # drag & drop.
        time.sleep(DEFAULT_UI_DELAY)
        paste('one-click')

        expected = exists(search_engine_pattern, 10)
        assert_true(self, expected, 'The \'One-Click Search Engines\' section found.')

        expected = exists(amazon_search_bar_pattern, 10)
        assert_true(self, expected, 'The \'Amazon\' search engine found in the page.')

        expected = exists(bing_search_bar_pattern, 10)
        assert_true(self, expected, 'The \'Bing\' search engine found in the page.')

        drag_drop(amazon_search_bar_pattern, bing_search_bar_pattern, 0.5)

        expected = exists(amazon_bing_pattern, 10)
        assert_true(self, expected, 'The drag and drop successfully performed.')

        # Open the drop down menu from the search fields available in about:newtab and from the Search Bar.
        new_tab()
        select_location_bar()
        type(Key.DOWN)

        expected = exists(amazon_bing_location_bar_pattern, 10)
        assert_true(self, expected, 'The search engine is placed correctly in location bar.')

        new_tab()
        expected = exists(google_logo_content_search_field_pattern, 10)
        assert_true(self, expected, 'Google logo from content search field found.')

        click(google_logo_content_search_field_pattern)
        type(Key.DOWN)

        expected = exists(amazon_bing_content_search_pattern, 10)
        assert_true(self, expected, 'The search engine is placed correctly in content search field.')

        select_search_bar()
        type(Key.DOWN)

        expected = exists(amazon_bing_search_bar_pattern, 10)
        assert_true(self, expected, 'The search engine is placed correctly in search bar.')
