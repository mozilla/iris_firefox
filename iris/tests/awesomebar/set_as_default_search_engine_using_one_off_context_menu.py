# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This test case verifies that \'Set as Default Search Engine\' option works correctly using an ' \
                    'one-off.'

    def run(self):
        moz = 'moz.png'
        url = LocalWeb.FIREFOX_TEST_SITE
        one_off_searches = 'one_off_searches.png'
        wikipedia_one_off_button = 'wikipedia_one_off_button.png'
        set_as_default_search_engine = 'set_as_default_search_engine.png'
        search_in_new_tab = 'search_in_new_tab.png'
        google_logo = 'google_logo.png'
        wikipedia_search_results = 'wikipedia_search_results.png'
        test = 'test.png'

        region = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        select_location_bar()
        paste('test')
        type(Key.ENTER)

        expected = region.exists(google_logo, 10)
        assert_true(self, expected, 'The default search engine is \'Google\'.')

        expected = region.exists(test, 10)
        assert_true(self, expected, 'Searched item is successfully found in the page opened by the default search '
                                    'engine.')

        select_location_bar()
        paste('moz')

        expected = region.exists(moz, 10)
        assert_true(self, expected, 'Searched string found at the bottom of the drop-down list.')

        expected = region.exists(one_off_searches, 10)
        assert_true(self, expected, 'The one-off searches are displayed in the awesome bar.')

        hover(wikipedia_one_off_button)

        try:
            expected = region.wait_vanish(moz, 10)
            assert_true(self, expected, 'The \'Wikipedia\' one-off button is highlighted.')
        except FindError:
            raise FindError('The \'Wikipedia\' one-off button is not highlighted.')

        right_click(wikipedia_one_off_button)

        expected = exists(search_in_new_tab, 10)
        assert_true(self, expected, 'The \'Search in New Tab\' option found.')

        expected = exists(set_as_default_search_engine, 10)
        assert_true(self, expected, 'The \'Set As Default Search Engine\' option found.')

        click(set_as_default_search_engine)
        time.sleep(DEFAULT_UI_DELAY_LONG)

        select_location_bar()
        paste('testing')
        type(Key.ENTER)

        expected = exists(wikipedia_search_results, 10)
        assert_true(self, expected, 'Wikipedia results are opened.')

        expected = exists('Test', 10)
        assert_true(self, expected, 'Searched item is successfully found in the page opened by the wikipedia search '
                                    'engine.')
