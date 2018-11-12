# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This test case checks the one-off search bar and the Settings gear after removing checks for ' \
                    'each search engine from the Search Settings.'
        self.test_case_id = '108259'
        self.test_suite_id = '1902'
        self.locales = ['en-US']

    def run(self):
        moz_pattern = Pattern('moz.png')
        url = LocalWeb.FIREFOX_TEST_SITE
        search_engine_pattern = Pattern('search_engine.png')
        check_engine_pattern = Pattern('check_engine.png')
        search_settings_pattern = Pattern('search_settings.png')
        amazon_one_off_button_pattern = Pattern('amazon_one_off_button.png')
        bing_one_off_button_pattern = Pattern('bing_one_off_button.png')
        duck_duck_go_one_off_button_pattern = Pattern('duck_duck_go_one_off_button.png')
        google_one_off_button_pattern = Pattern('google_one_off_button.png')
        twitter_one_off_button_pattern = Pattern('twitter_one_off_button.png')
        wikipedia_one_off_button_pattern = Pattern('wikipedia_one_off_button.png')
        about_preferences_search_page_pattern = Pattern('about_preferences_search_page.png')

        region = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)

        navigate(url)
        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        select_location_bar()
        paste('moz')

        pattern_list = [moz_pattern, search_settings_pattern, amazon_one_off_button_pattern,
                        bing_one_off_button_pattern, duck_duck_go_one_off_button_pattern, google_one_off_button_pattern,
                        twitter_one_off_button_pattern, wikipedia_one_off_button_pattern]

        # Check that the one-off list is displayed in the awesomebar by default.
        for i in range(pattern_list.__len__()):
            try:
                if Settings.get_os() == Platform.MAC:
                    expected = region.exists(pattern_list[i].similar(0.7), 10)
                    assert_true(self, expected, 'Element found at position ' + i.__str__() + ' in the list found.')
                else:
                    expected = region.exists(pattern_list[i].similar(0.9), 10)
                    assert_true(self, expected, 'Element found at position ' + i.__str__() + ' in the list found.')
            except FindError:
                raise FindError('Element found at position ' + i.__str__() + ' in the list not found.')

        click(search_settings_pattern)
        time.sleep(DEFAULT_UI_DELAY)

        expected = exists(about_preferences_search_page_pattern, 10)
        assert_true(self, expected, 'The \'about:preferences#search\' page successfully loaded.')

        paste('one-click')

        expected = exists(search_engine_pattern, 10)
        assert_true(self, expected, 'One-Click Search Engines section found.')

        # Uncheck all the search engines from the list.
        while exists(check_engine_pattern, 2):
            click(check_engine_pattern)

        try:
            expected = region.wait_vanish(check_engine_pattern.similar(0.9), 5)
            assert_true(self, expected, 'Each search engine is unchecked.')
        except FindError:
            raise FindError('There are search engines still checked.')

        new_tab()

        select_location_bar()
        paste('moz')

        # Check that the one-off list is not displayed in the awesomebar after each search engine was unchecked.
        for i in range(pattern_list.__len__()):
            try:
                expected = wait_vanish(pattern_list[i].similar(0.9), 10)
                assert_true(self, expected, 'Element found at position ' + i.__str__() + ' in the list not found.')
            except FindError:
                raise FindError('Element found at position ' + i.__str__() + ' in the list found.')
