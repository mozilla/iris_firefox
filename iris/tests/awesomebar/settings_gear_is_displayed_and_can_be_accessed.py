# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This test case checks that the Settings gear is displayed and can be accessed.'
        self.test_case_id = '108260'
        self.test_suite_id = '1902'
        self.locales = ['en-US']

    def run(self):
        url = LocalWeb.FIREFOX_TEST_SITE
        search_settings_pattern = Pattern('search_settings.png')
        settings_gear_options_pattern = Pattern('settings_gear_options.png')
        search_engine_pattern = Pattern('search_engine.png')

        region = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        select_location_bar()
        paste('moz')

        expected = region.exists(search_settings_pattern, 10)
        assert_true(self, expected, 'The \'Search settings\' button is displayed in the awesomebar.')

        right_click(search_settings_pattern)

        expected = exists(settings_gear_options_pattern, 5)
        assert_false(self, expected,
                     'The \'Search in new tab\' and \'Set as default search engine\' options not found.')

        # Click the Settings gear button to navigate to the 'about:preferences#search' page.
        click(search_settings_pattern)

        expected = exists(search_engine_pattern, 10)
        assert_true(self, expected, 'Successfully navigated to the \'about:preferences#search\' page.')

        # Close the 'about:preferences#search' page.
        close_tab()

        select_location_bar()
        type(Key.DELETE)
        paste('moz')

        expected = region.exists(search_settings_pattern, 10)
        assert_true(self, expected, 'The \'Search settings\' button is displayed in the awesomebar.')

        for i in range(17):
            type(Key.DOWN)

        type(Key.ENTER)

        expected = exists(search_engine_pattern, 10)
        assert_true(self, expected, 'Successfully navigated to the \'about:preferences#search\' page.')
