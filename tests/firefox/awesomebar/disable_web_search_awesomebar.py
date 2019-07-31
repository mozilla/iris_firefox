# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This test case disables the web search in the awesomebar.',
        locale=['en-US'],
        test_case_id='108254',
        test_suite_id='1902',
        preferences={'browser.contentblocking.enabled': False}
    )
    def run(self, firefox):
        google_one_off_button_pattern = Pattern('google_one_off_button.png')
        google_search_results_pattern = Pattern('google_search_results.png')
        search_with_url_autocomplete_pattern = Pattern('search_with_url_autocomplete.png')
        mozilla_support_url_pattern = Pattern('mozilla_support_url.png')
        amazon_logo_pattern = Pattern('amazon_logo.png')

        top_two_thirds_region = Region(0, 0, Screen.SCREEN_WIDTH, 2 * Screen.SCREEN_HEIGHT / 3)

        navigate('www.amazon.com')

        amazon_page_opened = exists(amazon_logo_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert amazon_page_opened, 'Page successfully loaded, amazon logo found.'

        select_location_bar()
        type('moz')

        one_off_button_exists = exists(google_one_off_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                                       region=top_two_thirds_region)
        assert one_off_button_exists, 'The \'Google\' one-off button found.'

        click(google_one_off_button_pattern)

        mozilla_support_url_exists = exists(mozilla_support_url_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                                            region=top_two_thirds_region)
        if mozilla_support_url_exists:
            select_location_bar()
            type('moz')
            time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
            click(google_one_off_button_pattern)
            time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)

        google_search_results_displayed = exists(google_search_results_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                                                 region=top_two_thirds_region)
        assert google_search_results_displayed, 'Google search results are displayed.'

        change_preference('keyword.enabled', 'false')

        select_location_bar()
        type('amaz')

        autocomplete_performed = exists(search_with_url_autocomplete_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                                        region=top_two_thirds_region)
        assert autocomplete_performed, 'Search is performed with url autocomplete for pages where you have been before.'

        type(Key.ENTER)

        amazon_page_opened = exists(amazon_logo_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert amazon_page_opened, 'Page successfully loaded, amazon logo found.'

        select_location_bar()
        type('test')

        google_one_off_button_found = exists(google_one_off_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                                             region=top_two_thirds_region)
        assert google_one_off_button_found, 'The \'Google\' one-off button found.'

        click(google_one_off_button_pattern)

        google_search_results_displayed = exists(google_search_results_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                                                 region=top_two_thirds_region)

        assert google_search_results_displayed, 'Google search results are displayed.'
