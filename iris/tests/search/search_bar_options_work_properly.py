# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'The options available for the Search Bar are working properly.'
        self.test_case_id = '4271'
        self.test_suite_id = '83'
        self.locale = ['en-US']

    def run(self):
        google_search_no_input_pattern = Pattern('google_search_no_input.png')
        change_search_settings_pattern = Pattern('change_search_settings.png')
        about_preferences_search_page_pattern = Pattern('about_preferences_search_page.png')
        default_search_engine_dropdown_pattern = Pattern('default_search_engine_dropdown.png')
        search_button_pattern = Pattern('search_button.png')
        test_pattern = Pattern('test.png')

        # Enable the search bar.
        change_preference('browser.search.widget.inNavBar', True)

        # Press enter without providing any input in the search bar.
        select_search_bar()
        type(Key.ENTER)

        expected = exists(google_search_no_input_pattern, 10)
        assert_true(self, expected, 'The search engine page is opened with no searches performed.')

        # Enter a word in the Search Bar and press enter.
        select_search_bar()
        paste('test')
        time.sleep(DEFAULT_UI_DELAY)
        type(Key.ENTER)

        expected = exists(test_pattern, 10)
        assert_true(self, expected,
                    'The search engine page is opened with search results available for the term in question.')

        # Change the default search engine.
        select_search_bar()
        expected = exists(change_search_settings_pattern, 10)
        assert_true(self, expected, 'The \'Change Search Settings\' button found in the page.')

        click(change_search_settings_pattern)

        expected = exists(about_preferences_search_page_pattern, 10)
        assert_true(self, expected, 'The \'about:preferences#search\' page opened.')

        click(default_search_engine_dropdown_pattern)
        repeat_key_down(2)
        type(Key.ENTER)

        # Perform a search from the search bar.
        select_search_bar()
        type(Key.ENTER)
        time.sleep(DEFAULT_UI_DELAY_LONG)

        select_location_bar()
        time.sleep(DEFAULT_UI_DELAY)
        edit_select_all()
        time.sleep(DEFAULT_UI_DELAY)
        edit_copy()
        time.sleep(DEFAULT_UI_DELAY_LONG)
        url_text = Env.get_clipboard()
        time.sleep(DEFAULT_UI_DELAY)

        assert_contains(self, url_text, 'https://www.amazon.com/',
                        'Search results are displayed using the newly search provider.')

        assert_contains(self, url_text, 'test',
                        'Search results are displayed for the searched term.')

        # Perform a search from the location bar.
        select_location_bar()
        paste('testing')
        time.sleep(DEFAULT_UI_DELAY)
        type(Key.ENTER)
        time.sleep(DEFAULT_UI_DELAY_LONG)

        select_location_bar()
        time.sleep(DEFAULT_UI_DELAY)
        edit_select_all()
        time.sleep(DEFAULT_UI_DELAY)
        edit_copy()
        time.sleep(DEFAULT_UI_DELAY_LONG)
        url_text = Env.get_clipboard()
        time.sleep(DEFAULT_UI_DELAY)

        assert_contains(self, url_text, 'https://www.amazon.com/',
                        'Search results are displayed using the newly search provider.')

        assert_contains(self, url_text, 'testing',
                        'Search results are displayed for the searched term.')

        # Perform a search from about:newtab page, content search field.
        new_tab()

        region_int = Screen.RIGHT_THIRD
        region = region_int.left_third()
        expected = region.exists(search_button_pattern, 10)
        assert_true(self, expected, 'Search button found.')

        region.click(search_button_pattern.target_offset(-50, 0))
        paste('mozilla')
        time.sleep(DEFAULT_UI_DELAY)
        type(Key.ENTER)
        time.sleep(DEFAULT_UI_DELAY_LONG)

        select_location_bar()
        time.sleep(DEFAULT_UI_DELAY)
        edit_select_all()
        time.sleep(DEFAULT_UI_DELAY)
        edit_copy()
        time.sleep(DEFAULT_UI_DELAY_LONG)
        url_text = Env.get_clipboard()
        time.sleep(DEFAULT_UI_DELAY)

        assert_contains(self, url_text, 'https://www.amazon.com/',
                        'Search results are displayed using the newly search provider.')

        assert_contains(self, url_text, 'mozilla',
                        'Search results are displayed for the searched term.')

        # Restart Firefox and check the default search engine.
        restart_firefox(self,
                        self.browser.path,
                        self.profile_path,
                        LocalWeb.FIREFOX_TEST_SITE,
                        image=LocalWeb.FIREFOX_LOGO)
        time.sleep(DEFAULT_UI_DELAY_LONG)

        select_search_bar()
        type(Key.ENTER)
        time.sleep(DEFAULT_UI_DELAY_LONG)

        select_location_bar()
        url_text = copy_to_clipboard()

        assert_equal(self, url_text, 'https://www.amazon.com/', 'The default search provider is kept after restart.')
