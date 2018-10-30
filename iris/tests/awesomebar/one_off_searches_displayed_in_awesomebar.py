# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This test case checks that one-off searches are displayed in the awesomebar.'
        self.test_case_id = '108248'
        self.test_suite_id = '1902'
        self.locales = ['en-US']

    def run(self):
        url = LocalWeb.FIREFOX_TEST_SITE
        search_settings_pattern = Pattern('search_settings.png')
        amazon_one_off_button_pattern = Pattern('amazon_one_off_button.png')
        bing_one_off_button_pattern = Pattern('bing_one_off_button.png')
        duck_duck_go_one_off_button_pattern = Pattern('duck_duck_go_one_off_button.png')
        google_one_off_button_pattern = Pattern('google_one_off_button.png')
        twitter_one_off_button_pattern = Pattern('twitter_one_off_button.png')
        wikipedia_one_off_button_pattern = Pattern('wikipedia_one_off_button.png')
        moz_pattern = Pattern('moz.png')

        region = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        select_location_bar()
        paste('moz')

        expected = region.exists(moz_pattern, 10)
        assert_true(self, expected, 'Searched string found at the bottom of the drop-down list.')

        expected = region.exists(search_settings_pattern, 10)
        assert_true(self, expected, 'The \'Search settings\' button is displayed in the awesomebar.')

        expected = region.exists(amazon_one_off_button_pattern.similar(0.7), 10)
        assert_true(self, expected, 'The \'Amazon\' one-off button found.')

        expected = region.exists(bing_one_off_button_pattern, 10)
        assert_true(self, expected, 'The \'Bing\' one-off button found.')

        expected = region.exists(duck_duck_go_one_off_button_pattern, 10)
        assert_true(self, expected, 'The \'DuckDuckGo\' one-off button found.')

        # Deactivated assert for ebay because we no longer have the ebay search engine in some locations.

        # expected = region.exists(ebay_one_off_button_pattern, 10)
        # assert_true(self, expected, 'The \'Ebay\' one-off button found.')

        expected = region.exists(google_one_off_button_pattern, 10)
        assert_true(self, expected, 'The \'Google\' one-off button found.')

        expected = region.exists(twitter_one_off_button_pattern, 10)
        assert_true(self, expected, 'The \'Twitter\' one-off button found.')

        expected = region.exists(wikipedia_one_off_button_pattern, 10)
        assert_true(self, expected, 'The \'Wikipedia\' one-off button found.')
