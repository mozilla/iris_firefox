# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This test case verifies that \'Set as Default Search Engine\' option works correctly using an ' \
                    'one-off.'
        self.test_case_id = '108251'
        self.test_suite_id = '1902'
        self.locales = ['en-US']

    def run(self):
        moz_pattern = Pattern('moz.png')
        url = LocalWeb.FIREFOX_TEST_SITE
        wikipedia_one_off_button_pattern = Pattern('wikipedia_one_off_button.png')
        set_as_default_search_engine_pattern = Pattern('set_as_default_search_engine.png')
        search_in_new_tab_pattern = Pattern('search_in_new_tab.png')
        magnifying_glass_pattern = Pattern('magnifying_glass.png')
        wikipedia_search_results_pattern = Pattern('wikipedia_search_results.png')
        test_pattern = Pattern('test.png').similar(0.5)

        region = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        select_location_bar()
        paste('test')
        type(Key.ENTER)
        time.sleep(DEFAULT_UI_DELAY_LONG)

        expected = region.exists(magnifying_glass_pattern, 10)
        assert_true(self, expected, 'The default search engine is \'Google\', page successfully loaded.')

        expected = region.exists(test_pattern, 10)
        assert_true(self, expected,
                    'Searched item is successfully found in the page opened by the default search engine.')

        select_location_bar()
        paste('moz')

        expected = region.exists(moz_pattern, 10)
        assert_true(self, expected, 'Searched string found at the bottom of the drop-down list.')

        hover(wikipedia_one_off_button_pattern)

        try:
            expected = region.wait_vanish(moz_pattern, 10)
            assert_true(self, expected, 'The \'Wikipedia\' one-off button is highlighted.')
        except FindError:
            raise FindError('The \'Wikipedia\' one-off button is not highlighted.')

        right_click(wikipedia_one_off_button_pattern)

        expected = exists(search_in_new_tab_pattern, 10)
        assert_true(self, expected, 'The \'Search in New Tab\' option found.')

        expected = exists(set_as_default_search_engine_pattern, 10)
        assert_true(self, expected, 'The \'Set As Default Search Engine\' option found.')

        click(set_as_default_search_engine_pattern)
        time.sleep(DEFAULT_UI_DELAY_LONG)

        select_location_bar()
        paste('testing')
        type(Key.ENTER)

        expected = exists(wikipedia_search_results_pattern, 10)
        assert_true(self, expected, 'Wikipedia results are opened.')

        expected = exists(test_pattern, 10)
        assert_true(self, expected,
                    'Searched item is successfully found in the page opened by the wikipedia search engine.')
