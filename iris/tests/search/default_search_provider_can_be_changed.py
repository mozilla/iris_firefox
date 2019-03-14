# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'The default search provider can be changed.'
        self.test_case_id = '4265'
        self.test_suite_id = '83'
        self.locale = ['en-US']

    def run(self):
        change_search_settings_pattern = Pattern('change_search_settings.png')
        about_preferences_search_page_pattern = Pattern('about_preferences_search_page.png')
        default_search_engine_dropdown_pattern = Pattern('default_search_engine_dropdown.png')

        change_preference('browser.search.widget.inNavBar', True)

        select_search_bar()
        paste('testing')

        expected = exists(change_search_settings_pattern, 10)
        assert_true(self, expected, 'The \'Change Search Settings\' button found in the page.')

        click(change_search_settings_pattern)

        expected = exists(about_preferences_search_page_pattern, 10)
        assert_true(self, expected, 'The \'about:preferences#search\' page opened.')

        click(default_search_engine_dropdown_pattern)
        repeat_key_down(2)
        type(Key.ENTER)

        select_search_bar()
        type(Key.ENTER)
        time.sleep(DEFAULT_UI_DELAY_LONG)

        select_location_bar()
        url_text = copy_to_clipboard()

        assert_contains(self, url_text, 'https://www.amazon.com/',
                        'Search results are displayed for the newly set default search provider.')

        assert_contains(self, url_text, 'testing',
                        'Search results are displayed for that search term.')
