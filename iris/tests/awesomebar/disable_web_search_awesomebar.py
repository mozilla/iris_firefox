# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This test case disables the web search in the awesomebar.'
        self.test_case_id = '108254'
        self.test_suite_id = '1902'
        self.locales = ['en-US']
        self.set_profile_pref({'browser.contentblocking.enabled': False})

    def run(self):
        google_one_off_button_pattern = Pattern('google_one_off_button.png')
        google_search_results_pattern = Pattern('google_search_results.png')
        search_with_url_autocomplete_pattern = Pattern('search_with_url_autocomplete.png')
        default_status_pattern = Pattern('default_status.png')
        modified_status_pattern = Pattern('modified_status.png')
        mozilla_support_url_pattern = Pattern('mozilla_support_url.png')
        true_value_pattern = Pattern('true_value.png')
        false_value_pattern = Pattern('false_value.png')
        amazon_logo_pattern = Pattern('amazon_logo.png')
        accept_risk_pattern = Pattern('accept_risk.png')

        region = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)

        navigate('www.amazon.com')

        close_content_blocking_pop_up()

        expected = exists(amazon_logo_pattern, 10)
        assert_true(self, expected, 'Page successfully loaded, amazon logo found.')

        select_location_bar()
        paste('moz')

        expected = region.exists(google_one_off_button_pattern, 10)
        assert_true(self, expected, 'The \'Google\' one-off button found.')

        time.sleep(DEFAULT_UI_DELAY_LONG)

        click(google_one_off_button_pattern)

        time.sleep(DEFAULT_UI_DELAY_LONG)

        # From time to time user is redirected to the Mozilla support page instead of the Google page. If this happens
        # we will repeat the search.
        expected = region.exists(mozilla_support_url_pattern, 10)
        if expected:
            select_location_bar()
            paste('moz')
            time.sleep(DEFAULT_UI_DELAY_LONG)
            click(google_one_off_button_pattern)
            time.sleep(DEFAULT_UI_DELAY_LONG)

        expected = region.exists(google_search_results_pattern, 10)
        assert_true(self, expected, 'Google search results are displayed.')

        navigate('about:config')

        # Change focus from the url bar.
        if Settings.get_os() == Platform.WINDOWS or Settings.get_os() == Platform.LINUX:
            click(NavBar.HAMBURGER_MENU.target_offset(-170, 15))
            type(Key.ENTER)
        else:
            click(accept_risk_pattern)

        expected = region.exists(default_status_pattern, 10)
        assert_true(self, expected, 'The \'about:config\' page successfully loaded and default status is correct.')

        paste('keyword.enabled')
        type(Key.ENTER)

        expected = region.exists(default_status_pattern, 10)
        assert_true(self, expected, 'The \'keyword.enabled\' preference has status \'default\' by default.')

        expected = region.exists(true_value_pattern, 10)
        assert_true(self, expected, 'The \'keyword.enabled\' preference has value \'true\' by default.')

        double_click(default_status_pattern)

        expected = region.exists(modified_status_pattern, 10)
        assert_true(self, expected,
                    'The \'keyword.enabled\' preference has status \'modified\' after the preference has changed.')

        expected = region.exists(false_value_pattern, 10)
        assert_true(self, expected,
                    'The \'keyword.enabled\' preference has value \'false\' after the preference has changed.')

        select_location_bar()
        paste('amaz')

        expected = region.exists(search_with_url_autocomplete_pattern, 10)
        assert_true(self, expected, 'Search is performed with url autocomplete for pages where you have been before.')

        type(Key.ENTER)

        expected = exists(amazon_logo_pattern, 10)
        assert_true(self, expected, 'Page successfully loaded, amazon logo found.')

        # Perform a search using the same engine as the one used above.
        select_location_bar()
        paste('test')

        expected = region.exists(google_one_off_button_pattern, 10)
        assert_true(self, expected, 'The \'Google\' one-off button found.')

        click(google_one_off_button_pattern)
        time.sleep(DEFAULT_UI_DELAY_LONG)

        expected = region.exists(google_search_results_pattern, 10)
        assert_true(self, expected, 'Google search results are displayed.')
