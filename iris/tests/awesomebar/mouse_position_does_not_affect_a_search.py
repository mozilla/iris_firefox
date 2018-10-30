# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This test case checks that mouse position does not affect a search from awesomebar.'
        self.test_case_id = '108256'
        self.test_suite_id = '1902'
        self.locales = ['en-US']

    def run(self):
        url = LocalWeb.FIREFOX_TEST_SITE
        duck_duck_go_one_off_button = Pattern('duck_duck_go_one_off_button.png')
        google_search_results = Pattern('google_search_results.png')
        localhost = Pattern('localhost.png')
        hover_duck_duck_go_one_off_button = Pattern('hover_duck_duck_go_one_off_button.png')

        region = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        select_location_bar()
        paste('moz')

        expected = region.exists(duck_duck_go_one_off_button, 10)
        assert_true(self, expected, 'The \'DuckDuckGo\' one-off button found.')

        # Find the coordinates of the one-off button.
        coord = find(duck_duck_go_one_off_button)

        # In a new tab place the mouse cursor at a position that will later match position of a search
        # engine(e.g 'DuckDuckGo') icon in the awesomebar autocomplete area.
        new_tab()
        select_location_bar()

        # Type a partial part of the above address.
        type('127')

        expected = region.exists(localhost, 10)
        assert_true(self, expected, 'Searched string found at the bottom of the drop-down list.')

        hover(coord)

        expected = exists(hover_duck_duck_go_one_off_button, 10)
        assert_true(self, expected, 'Mouse is over the \'DuckDuckGo\' search engine.')

        # Press the 'arrow down' key to focus a page result.
        scroll_down()

        type(Key.ENTER)

        expected = exists(google_search_results, 10)
        assert_true(self, expected, 'The browser does NOT search using the search engine that had the mouse over it, '
                                    'search is performed with the default search engine which is \'Google\'')
