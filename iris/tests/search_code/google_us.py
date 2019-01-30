# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Default Search Code: Google.'
        self.test_case_id = '218333'
        self.test_suite_id = '83'
        self.locales = ['en-US', 'de', 'fr', 'pl', 'it', 'br', 'ja', 'es-ES', 'en-GB']

        # iris -f [channel] -l [locale] -t [test case name]

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.BRAND_NEW
        self.set_profile_pref({'browser.search.region': 'en-US'})

    def run(self):
        default_search_engine_google_pattern = Pattern('default_search_engine_google.png')
        add_search_bar_in_toolbar_pattern = Pattern('add_search_bar_in_toolbar.png')
        search_bar_pattern = Pattern('search_bar.png')
        client_search_code_en_us_pattern = Pattern('client_search_code_en_us.png')

        # Channel: release; Locale: en-US:
        navigate('about:preferences#search')

        expected = exists(default_search_engine_google_pattern, 10)
        assert_true(self, expected, 'Google is the default search engine for the en-US locale.')

        expected = exists(add_search_bar_in_toolbar_pattern, 10)
        assert_true(self, expected, '\'Add search bar in toolbar\' option is visible in the page.')

        click(add_search_bar_in_toolbar_pattern)

        expected = exists(search_bar_pattern, 10)
        assert_true(self, expected, 'The search bar is properly enabled in toolbar.')

        # Perform a search using the awesome bar and then clear the content from it.
        select_location_bar()
        paste('test')
        type(Key.ENTER)

        expected = exists(client_search_code_en_us_pattern, 10)
        assert_true(self, expected, '\'client=firefox-b-1-d\' is the client search code for the en-US locale.')

        select_location_bar()
        type(Key.DELETE)

        # Perform a search using the search bar.
        click(search_bar_pattern)
        paste('test')
        type(Key.ENTER)

        expected = exists(client_search_code_en_us_pattern, 10)
        assert_true(self, expected, '\'client=firefox-b-1-d\' is the client search code for the en-US locale.')

        close_content_blocking_pop_up()
      