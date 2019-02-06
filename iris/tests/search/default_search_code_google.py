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

    def run(self):
        url = LocalWeb.FOCUS_TEST_SITE
        text_pattern = Pattern('focus_text.png')

        # Detect the build.
        if get_firefox_channel(self.browser.path) == 'beta':
            default_search_engine_google_pattern = Pattern('default_search_engine_google.png')
            client_search_code_pattern = Pattern('client_search_code.png').similar(0.9)
            non_us_client_search_code_pattern = Pattern('non_us_client_search_code.png')
        elif get_firefox_channel(self.browser.path) == 'esr':
            default_search_engine_google_pattern = Pattern('default_search_engine_google_esr_build.png')
            client_search_code_pattern = Pattern('client_search_code_esr_build.png').similar(0.9)
            non_us_client_search_code_pattern = Pattern('non_us_client_search_code_esr_build.png')

        regions_by_locales = {'en-US': ['US', 'in', 'id', 'ca'], 'de': ['de'], 'fr': ['fr'], 'pl': ['pl'], 'it': ['it'],
                              'pt-BR': ['BR'], 'ja': ['ja'], 'es-ES': ['ES'], 'en-GB': ['GB']}

        change_preference('browser.search.widget.inNavBar', True)

        # Detect the locale.
        for value in regions_by_locales.get(self.browser.locale):
            change_preference('browser.search.region', value)
            restart_firefox(self,
                            self.browser.path,
                            self.profile_path,
                            LocalWeb.FIREFOX_TEST_SITE,
                            image=LocalWeb.FIREFOX_LOGO)

            navigate('about:preferences#search')
            expected = exists(default_search_engine_google_pattern, 10)
            assert_true(self, expected, 'Google is the default search engine.')

            # Perform a search using the awesome bar and then clear the content from it.
            select_location_bar()
            paste('test')
            type(Key.ENTER)

            if value != 'US':
                expected = exists(non_us_client_search_code_pattern, 10)
                assert_true(self, expected, 'Client search code is correct for searches from awesome bar.')
            else:
                expected = exists(client_search_code_pattern, 10)
                assert_true(self, expected, 'Client search code is correct for searches from awesome bar.')

            select_location_bar()
            type(Key.DELETE)

            # Perform a search using the search bar.
            select_search_bar()
            paste('test')
            type(Key.ENTER)

            if value != 'US':
                expected = exists(non_us_client_search_code_pattern, 10)
                assert_true(self, expected, 'Client search code is correct for searches from search bar.')
            else:
                expected = exists(client_search_code_pattern, 10)
                assert_true(self, expected, 'Client search code is correct for searches from search bar.')

            navigate(url)
            expected = exists(text_pattern, 10)
            assert_true(self, expected, 'Page successfully loaded, focus text found.')

            double_click(text_pattern)
            right_click(text_pattern)

            for i in range(3):
                type(Key.DOWN)
            type(Key.ENTER)
            time.sleep(DEFAULT_UI_DELAY)

            if value != 'US':
                expected = exists(non_us_client_search_code_pattern, 10)
                assert_true(self, expected, 'Client search code is correct.')
            else:
                expected = exists(client_search_code_pattern, 10)
                assert_true(self, expected, 'Client search code is correct.')

            new_tab()
            paste('test')
            type(Key.ENTER)

            if value != 'US':
                expected = exists(non_us_client_search_code_pattern, 10)
                assert_true(self, expected, 'Client search code is correct for searches from about:newtab page.')
            else:
                expected = exists(client_search_code_pattern, 10)
                assert_true(self, expected, 'Client search code is correct for searches from about:newtab page.')

    def teardown(self):
        if self.browser.locale == 'en-US':
            change_preference('browser.search.region', 'US')
