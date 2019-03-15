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
        self.locale = ['en-US', 'de', 'fr', 'pl', 'it', 'pt-BR', 'ja', 'es-ES', 'en-GB', 'ru']

    def run(self):
        url = LocalWeb.FOCUS_TEST_SITE
        text_pattern = Pattern('focus_text.png')
        text_pattern_selected = Pattern('focus_text_selected.png')

        # Detect the build.
        if get_firefox_channel(self.browser.path) == 'beta' or get_firefox_channel(self.browser.path) == 'release':
            default_search_engine_google_pattern = Pattern('default_search_engine_google.png')
            google_logo_content_search_field_pattern = Pattern('google_logo_content_search_field.png')
        elif get_firefox_channel(self.browser.path) == 'esr':
            default_search_engine_google_pattern = Pattern('default_search_engine_google_esr_build.png')
            google_logo_content_search_field_pattern = Pattern('google_logo_content_search_field_esr_build.png')

        regions_by_locales = {'en-US': ['US', 'in', 'id', 'ca'], 'de': ['de', 'ru'], 'fr': ['fr'], 'pl': ['pl'],
                              'it': ['it'], 'pt-BR': ['BR'], 'ja': ['ja'], 'es-ES': ['ES'], 'en-GB': ['GB'],
                              'ru': ['de']}

        change_preference('browser.search.widget.inNavBar', True)

        # Detect the locale.
        for value in regions_by_locales.get(self.browser.locale):
            change_preference('browser.search.region', value)
            restart_firefox(self,
                            self.browser.path,
                            self.profile_path,
                            LocalWeb.FIREFOX_TEST_SITE,
                            image=LocalWeb.FIREFOX_LOGO)
            time.sleep(DEFAULT_UI_DELAY_LONG)

            navigate('about:preferences#search')
            expected = exists(default_search_engine_google_pattern, 10)
            assert_true(self, expected, 'Google is the default search engine.')

            # Perform a search using the awesome bar and then clear the content from it.
            select_location_bar()
            paste('test')
            type(Key.ENTER)
            time.sleep(DEFAULT_UI_DELAY_LONG)
            select_location_bar()
            url_text = copy_to_clipboard()

            if get_firefox_channel(self.browser.path) == 'beta' or get_firefox_channel(self.browser.path) == 'release':
                if value != 'US':
                    assert_equal(self, url_text, 'https://www.google.com/search?client=firefox-b-d&q=test',
                                 'Client search code is correct for searches from awesome bar, region ' + value + '.')
                else:
                    assert_equal(self, url_text, 'https://www.google.com/search?client=firefox-b-1-d&q=test',
                                 'Client search code is correct for searches from awesome bar, region ' + value + '.')
            elif get_firefox_channel(self.browser.path) == 'esr':
                if value != 'US':
                    assert_equal(self, url_text,
                                 'https://www.google.com/search?q=test&ie=utf-8&oe=utf-8&client=firefox-b-e',
                                 'Client search code is correct for searches from awesome bar, region ' + value + '.')
                else:
                    assert_equal(self, url_text,
                                 'https://www.google.com/search?q=test&ie=utf-8&oe=utf-8&client=firefox-b-1-e',
                                 'Client search code is correct for searches from awesome bar, region ' + value + '.')

            select_location_bar()
            type(Key.DELETE)

            # Perform a search using the search bar.
            select_search_bar()
            paste('test')
            type(Key.ENTER)
            time.sleep(DEFAULT_UI_DELAY_LONG)
            select_location_bar()
            url_text = copy_to_clipboard()

            if get_firefox_channel(self.browser.path) == 'beta' or get_firefox_channel(self.browser.path) == 'release':
                if value != 'US':
                    assert_equal(self, url_text, 'https://www.google.com/search?client=firefox-b-d&q=test',
                                 'Client search code is correct for searches from search bar, region ' + value + '.')
                else:
                    assert_equal(self, url_text, 'https://www.google.com/search?client=firefox-b-1-d&q=test',
                                 'Client search code is correct for searches from search bar, region ' + value + '.')
            elif get_firefox_channel(self.browser.path) == 'esr':
                if value != 'US':
                    assert_equal(self, url_text,
                                 'https://www.google.com/search?q=test&ie=utf-8&oe=utf-8&client=firefox-b-e',
                                 'Client search code is correct for searches from search bar, region ' + value + '.')
                else:
                    assert_equal(self, url_text,
                                 'https://www.google.com/search?q=test&ie=utf-8&oe=utf-8&client=firefox-b-1-e',
                                 'Client search code is correct for searches from search bar, region ' + value + '.')

            # Highlight some text and right click it.
            new_tab()
            navigate(url)
            expected = exists(text_pattern, 50)
            assert_true(self, expected, 'Page successfully loaded, focus text found.')

            double_click(text_pattern)
            time.sleep(DEFAULT_UI_DELAY_LONG)
            right_click(text_pattern_selected)
            time.sleep(DEFAULT_UI_DELAY)
            repeat_key_down(3)
            type(Key.ENTER)
            time.sleep(DEFAULT_UI_DELAY_LONG)
            select_location_bar()
            url_text = copy_to_clipboard()

            if get_firefox_channel(self.browser.path) == 'beta' or get_firefox_channel(self.browser.path) == 'release':
                if value != 'US':
                    assert_equal(self, url_text, 'https://www.google.com/search?client=firefox-b-d&q=Focus',
                                 'Client search code is correct, region ' + value + '.')
                else:
                    assert_equal(self, url_text, 'https://www.google.com/search?client=firefox-b-1-d&q=Focus',
                                 'Client search code is correct, region ' + value + '.')
            elif get_firefox_channel(self.browser.path) == 'esr':
                if value != 'US':
                    assert_equal(self, url_text,
                                 'https://www.google.com/search?q=Focus&ie=utf-8&oe=utf-8&client=firefox-b-e',
                                 'Client search code is correct, region ' + value + '.')
                else:
                    assert_equal(self, url_text,
                                 'https://www.google.com/search?q=Focus&ie=utf-8&oe=utf-8&client=firefox-b-1-e',
                                 'Client search code is correct, region ' + value + '.')

            # Perform a search from about:newtab page, content search field.
            new_tab()
            expected = exists(google_logo_content_search_field_pattern, 10)
            assert_true(self, expected, 'Google logo from content search field found.')
            click(google_logo_content_search_field_pattern)
            paste('beats')
            type(Key.ENTER)
            time.sleep(DEFAULT_UI_DELAY_LONG)
            select_location_bar()
            url_text = copy_to_clipboard()

            if get_firefox_channel(self.browser.path) == 'beta' or get_firefox_channel(self.browser.path) == 'release':
                if value != 'US':
                    assert_equal(self, url_text, 'https://www.google.com/search?client=firefox-b-d&q=beats',
                                 'Client search code is correct for searches from about:newtab page, content search '
                                 'field, region ' + value + '.')
                else:
                    assert_equal(self, url_text, 'https://www.google.com/search?client=firefox-b-1-d&q=beats',
                                 'Client search code is correct for searches from about:newtab page, content search '
                                 'field, region ' + value + '.')
            elif get_firefox_channel(self.browser.path) == 'esr':
                if value != 'US':
                    assert_equal(self, url_text,
                                 'https://www.google.com/search?q=beats&ie=utf-8&oe=utf-8&client=firefox-b-e',
                                 'Client search code is correct for searches from about:newtab page, content search '
                                 'field, region ' + value + '.')
                else:
                    assert_equal(self, url_text,
                                 'https://www.google.com/search?q=beats&ie=utf-8&oe=utf-8&client=firefox-b-1-e',
                                 'Client search code is correct for searches from about:newtab page, content search '
                                 'field, region ' + value + '.')

    def teardown(self):
        if self.browser.locale == 'en-US':
            change_preference('browser.search.region', 'US')
