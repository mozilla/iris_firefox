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

    # def setup(self):
    #     BaseTest.setup(self)
    #     self.set_profile_pref({'browser.search.region': 'US'})

    def run(self):
        # Detect the build.
        if get_firefox_channel(self.browser.path) == 'beta':
            test_pattern = Pattern('test.png')
            default_search_engine_google_pattern = Pattern('default_search_engine_google.png')
            add_search_bar_in_toolbar_pattern = Pattern('add_search_bar_in_toolbar.png')
            search_bar_pattern = Pattern('search_bar.png').similar(0.9)
            client_search_code_pattern = Pattern('client_search_code.png').similar(0.9)
            search_google_for_pattern = Pattern('search_google_for.png')
            non_us_client_search_code_pattern = Pattern('non_us_client_search_code.png')
        elif get_firefox_channel(self.browser.path) == 'esr':
            test_pattern = Pattern('test_esr_build.png')
            default_search_engine_google_pattern = Pattern('default_search_engine_google_esr_build.png')
            add_search_bar_in_toolbar_pattern = Pattern('add_search_bar_in_toolbar_esr_build.png')
            search_bar_pattern = Pattern('search_bar_esr_build.png').similar(0.9)
            client_search_code_pattern = Pattern('client_search_code_esr_build.png').similar(0.9)
            search_google_for_pattern = Pattern('search_google_for_esr_build.png')
            non_us_client_search_code_pattern = Pattern('non_us_client_search_code_esr_build.png')

        firefoxes = {'en-US': ['US','in', 'id', 'ca'], 'de': ['de'], 'fr': ['fr'], 'pl': ['pl'], 'it': ['it'],
                     'pt-BR': ['BR'], 'ja': ['ja'], 'es-ES': ['ES'], 'en-GB': ['GB']}

        for key in firefoxes.keys():
            for value in firefoxes.get(key):
                navigate('about:preferences#search')
                expected = exists(default_search_engine_google_pattern, 10)
                assert_true(self, expected, 'Google is the default search engine.')

                expected = exists(add_search_bar_in_toolbar_pattern, 10)
                assert_true(self, expected, 'Option is visible in the page.')

                click(add_search_bar_in_toolbar_pattern)

                expected = exists(search_bar_pattern, 10)
                assert_true(self, expected, 'The search bar is properly enabled in toolbar.')

                # Perform a search using the awesome bar and then clear the content from it.
                select_location_bar()
                paste('test')
                type(Key.ENTER)

                expected = exists(client_search_code_pattern, 10)
                assert_true(self, expected, 'Client search code is correct for searches from awesome bar.')

                select_location_bar()
                type(Key.DELETE)

                # Perform a search using the search bar.
                click(search_bar_pattern)
                paste('test')
                type(Key.ENTER)

                expected = exists(client_search_code_pattern, 10)
                assert_true(self, expected, 'Client search code is correct for searches from search bar.')

                select_location_bar()
                type(Key.DELETE)

                close_content_blocking_pop_up()

                double_click(test_pattern)
                right_click(test_pattern)

                expected = exists(search_google_for_pattern, 10)
                assert_true(self, expected, 'Option is visible.')

                click(search_google_for_pattern)
                time.sleep(DEFAULT_UI_DELAY)

                expected = exists(client_search_code_pattern, 10)
                assert_true(self, expected, 'Client search code is correct.')

                new_tab()
                paste('test')
                type(Key.ENTER)

                expected = exists(client_search_code_pattern, 10)
                assert_true(self, expected, 'Client search code is correct for searches from about:newtab page.')

                change_preference('browser.search.region', value)
                restart_firefox(self,
                                self.browser.path,
                                self.profile_path,
                                LocalWeb.FIREFOX_TEST_SITE,
                                image=LocalWeb.FIREFOX_LOGO)
