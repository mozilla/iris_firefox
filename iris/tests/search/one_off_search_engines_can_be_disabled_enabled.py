# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Items from the list of one-click search engines can be disabled and enabled.'
        self.test_case_id = '4275'
        self.test_suite_id = '83'
        self.locale = ['en-US']

    def run(self):
        change_search_settings_pattern = Pattern('change_search_settings.png')
        about_preferences_search_page_pattern = Pattern('about_preferences_search_page.png')
        amazon_search_bar_pattern = Pattern('amazon_search_bar.png')
        bing_search_bar_pattern = Pattern('bing_search_bar.png')
        duckduckgo_search_bar_pattern = Pattern('duckduckgo_search_bar.png')
        search_engine_pattern = Pattern('search_engine.png')
        check_engine_pattern = Pattern('check_engine.png').similar(0.7)
        test_search_bing_pattern = Pattern('test_search_bing.png')

        # Enable the search bar.
        change_preference('browser.search.widget.inNavBar', True)

        pattern_list = [amazon_search_bar_pattern, bing_search_bar_pattern, duckduckgo_search_bar_pattern]

        # Navigate to the 'about:preferences#search' page.
        select_search_bar()
        type(Key.DOWN)

        expected = exists(change_search_settings_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, expected, 'The \'Change Search Settings\' button found in the page.')

        click(change_search_settings_pattern)

        expected = exists(about_preferences_search_page_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, expected, 'The \'about:preferences#search\' page opened.')

        # Deselect several search engines from the One-click search engines list.
        paste('one-click')

        expected = exists(search_engine_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, expected, 'The \'One-Click Search Engines\' section found.')

        expected = exists(check_engine_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, expected, 'The check engine pattern found in the page.')

        region_int = Screen.LEFT_THIRD
        region = region_int.middle_third_horizontal()

        while region.exists(check_engine_pattern, Settings.TINY_FIREFOX_TIMEOUT):
            click(check_engine_pattern)

        try:
            expected = wait_vanish(check_engine_pattern, Settings.SHORT_FIREFOX_TIMEOUT, region)
            assert_true(self, expected, 'Each search engine is unchecked.')
        except FindError:
            raise FindError('There are search engines still checked.')

        # Perform a search from a new tab and a private window.
        # Check that the unchecked search engines are no longer displayed in the search bar, one-offs list.
        new_tab()

        select_search_bar()
        type(Key.DOWN)

        for i in range(pattern_list.__len__()):
            try:
                expected = wait_vanish(pattern_list[i], Settings.FIREFOX_TIMEOUT)
                assert_true(self, expected, 'Element found at position ' + i.__str__() + ' in the list not found.')

            except FindError:
                raise FindError('Element found at position ' + i.__str__() + ' in the list found.')

        new_private_window()

        select_search_bar()
        type(Key.DOWN)

        for i in range(pattern_list.__len__()):
            try:
                expected = wait_vanish(pattern_list[i], Settings.FIREFOX_TIMEOUT)
                assert_true(self, expected, 'Element found at position ' + i.__str__() + ' in the list not found.')

            except FindError:
                raise FindError('Element found at position ' + i.__str__() + ' in the list found.')

        close_window()

        # Select again 'Change Search Settings' and enable back the search engines.
        select_search_bar()
        type(Key.DOWN)

        click(change_search_settings_pattern)

        expected = exists(about_preferences_search_page_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, expected, 'The \'about:preferences#search\' page opened.')

        type(Key.TAB)

        click(amazon_search_bar_pattern.target_offset(-10, 5))

        click(bing_search_bar_pattern.target_offset(-10, 5))

        click(duckduckgo_search_bar_pattern.target_offset(-10, 5))

        # Repeat the above steps to see that the search engines are restored.
        region = Screen.UPPER_RIGHT_CORNER

        new_tab()

        select_search_bar()
        paste('test')

        for i in range(pattern_list.__len__()):
            try:
                expected = region.exists(pattern_list[i], Settings.FIREFOX_TIMEOUT)
                assert_true(self, expected, 'Element found at position ' + i.__str__() + ' in the list found.')

            except FindError:
                raise FindError('Element found at position ' + i.__str__() + ' in the list not found.')

        new_private_window()

        select_search_bar()
        type(Key.DOWN)

        for i in range(pattern_list.__len__()):
            try:
                expected = region.exists(pattern_list[i], 10)
                assert_true(self, expected, 'Element found at position ' + i.__str__() + ' in the list found.')

            except FindError:
                raise FindError('Element found at position ' + i.__str__() + ' in the list not found.')

        close_window()

        # Perform a search using a restored one-off search engine.
        type(Key.DOWN)

        region.click(bing_search_bar_pattern)

        time.sleep(Settings.TINY_FIREFOX_TIMEOUT)

        expected = exists(test_search_bing_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, expected, 'The search is performed with the Bing engine.')
