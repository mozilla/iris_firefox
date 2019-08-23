# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This test case verifies that \'Set as Default Search Engine\' option works correctly using an '
                    'one-off.',
        locale=['en-US'],
        test_case_id='108251',
        test_suite_id='1902',
        preferences={'browser.contentblocking.enabled': False}
    )
    def run(self, firefox):
        moz_pattern = Pattern('moz.png')
        url = LocalWeb.FIREFOX_TEST_SITE
        wikipedia_one_off_button_pattern = Pattern('wikipedia_one_off_button.png').similar(.7)
        set_as_default_search_engine_pattern = Pattern('set_as_default_search_engine.png')
        search_in_new_tab_pattern = Pattern('search_in_new_tab.png')
        magnifying_glass_pattern = Pattern('magnifying_glass.png').similar(.7)
        wikipedia_search_results_pattern = Pattern('wikipedia_search_results.png')
        test_pattern = Pattern('test.png')
        region = Region(0, 0, Screen().width, 2 * Screen().height / 3)

        navigate(url)

        test_page_opened = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert test_page_opened, 'Page successfully loaded, firefox logo found.'

        select_location_bar()
        paste('test')
        type(Key.ENTER)

        google_page_opened = region.exists(magnifying_glass_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert google_page_opened, 'The default search engine is \'Google\', page successfully loaded.'

        searched_item_found = region.exists(test_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert searched_item_found, 'Searched item is successfully found in the page opened by the default ' \
                                    'search engine.'

        select_location_bar()
        paste('moz')

        mozilla_pattern_displayed = region.exists(moz_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_pattern_displayed, 'Searched string found at the bottom of the drop-down list.'

        wiki_button_displayed = region.exists(wikipedia_one_off_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert wiki_button_displayed, 'wikipedia_one_off_button_pattern'

        right_click(wikipedia_one_off_button_pattern)

        search_in_new_tab_displayed = exists(search_in_new_tab_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert search_in_new_tab_displayed, 'The \'Search in New Tab\' option found.'

        set_as_default_displayed = exists(set_as_default_search_engine_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert set_as_default_displayed, 'The \'Set As Default Search Engine\' option found.'

        click(set_as_default_search_engine_pattern)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)

        select_location_bar()
        paste('test')
        type(Key.ENTER)

        wiki_page_opened = exists(wikipedia_search_results_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert wiki_page_opened, 'Wikipedia results are opened.'

        searched_item_found = exists('Test', FirefoxSettings.FIREFOX_TIMEOUT)
        assert searched_item_found, 'Searched item is successfully found in the page opened by the wikipedia ' \
                                    'search engine.'
