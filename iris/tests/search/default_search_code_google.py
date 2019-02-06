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
        elif get_firefox_channel(self.browser.path) == 'esr':
            default_search_engine_google_pattern = Pattern('default_search_engine_google_esr_build.png')

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
            time.sleep(DEFAULT_UI_DELAY_LONG)
            select_location_bar()
            time.sleep(DEFAULT_UI_DELAY)
            edit_copy()
            time.sleep(DEFAULT_UI_DELAY)
            url_text = Env.get_clipboard()

            if value != 'US':
                assert_equal(self, url_text, 'https://www.google.com/search?client=firefox-b-d&q=test',
                            'Client search code is correct for searches from awesome bar.')
            else:
                assert_equal(self, url_text, 'https://www.google.com/search?client=firefox-b-1-d&q=test',
                            'Client search code is correct for searches from awesome bar.')

            select_location_bar()
            type(Key.DELETE)

            # Perform a search using the search bar.
            select_search_bar()
            paste('test')
            type(Key.ENTER)
            time.sleep(DEFAULT_UI_DELAY_LONG)
            select_location_bar()
            time.sleep(DEFAULT_UI_DELAY)
            edit_copy()
            time.sleep(DEFAULT_UI_DELAY)
            url_text = Env.get_clipboard()

            if value != 'US':
                assert_equal(self, url_text, 'https://www.google.com/search?client=firefox-b-d&q=test',
                            'Client search code is correct for searches from awesome bar.')
            else:
                assert_equal(self, url_text, 'https://www.google.com/search?client=firefox-b-1-d&q=test',
                            'Client search code is correct for searches from awesome bar.')

            navigate(url)
            expected = exists(text_pattern, 10)
            assert_true(self, expected, 'Page successfully loaded, focus text found.')

            double_click(text_pattern)
            right_click(text_pattern)
            time.sleep(DEFAULT_FX_DELAY)
            repeat_key_down(3)
            type(Key.ENTER)
            time.sleep(DEFAULT_UI_DELAY_LONG)
            select_location_bar()
            time.sleep(DEFAULT_UI_DELAY)
            edit_copy()
            time.sleep(DEFAULT_UI_DELAY)
            url_text = Env.get_clipboard()

            if value != 'US':
                assert_equal(self, url_text, 'https://www.google.com/search?client=firefox-b-d&q=Focus',
                            'Client search code is correct for searches from awesome bar.')
            else:
                assert_equal(self, url_text, 'https://www.google.com/search?client=firefox-b-1-d&q=Focus',
                            'Client search code is correct for searches from awesome bar.')

            new_tab()
            # Ioana, please add code here to find and click the "G" logo. Then continue on with paste.
            paste('beats')
            type(Key.ENTER)
            time.sleep(DEFAULT_UI_DELAY_LONG)
            select_location_bar()
            time.sleep(DEFAULT_UI_DELAY)
            edit_copy()
            time.sleep(DEFAULT_UI_DELAY)
            url_text = Env.get_clipboard()

            if value != 'US':
                assert_equal(self, url_text, 'https://www.google.com/search?client=firefox-b-d&q=beats',
                            'Client search code is correct for searches from awesome bar.')
            else:
                assert_equal(self, url_text, 'https://www.google.com/search?client=firefox-b-1-d&q=beats',
                            'Client search code is correct for searches from awesome bar.')

    def teardown(self):
        if self.browser.locale == 'en-US':
            change_preference('browser.search.region', 'US')
