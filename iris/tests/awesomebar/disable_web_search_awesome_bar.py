# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This test case disables the web search in the awesome bar.'
        # Disabled test for running on MAC until issue #950 is fixed.
        self.exclude = Platform.MAC

    def run(self):
        google_one_off_button = Pattern('google_one_off_button.png')
        google_search_results = Pattern('google_search_results.png')
        search_with_url_autocomplete = Pattern('search_with_url_autocomplete.png')
        default_status = Pattern('default_status.png')
        modified_status = Pattern('modified_status.png')
        true_value = Pattern('true_value.png')
        false_value = Pattern('false_value.png')
        amazon_logo = Pattern('amazon_logo.png')
        accept_risk = Pattern('accept_risk.png')

        region = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)

        navigate('www.amazon.com')

        expected = exists(amazon_logo, 10)
        assert_true(self, expected, 'Page successfully loaded, amazon logo found.')

        select_location_bar()
        paste('moz')

        expected = region.exists(google_one_off_button, 10)
        assert_true(self, expected, 'The \'Google\' one-off button found.')

        click(google_one_off_button)
        time.sleep(DEFAULT_UI_DELAY_LONG)

        expected = region.exists(google_search_results, 10)
        assert_true(self, expected, 'Google search results are displayed.')

        navigate('about:config')

        # Change focus from the url bar.
        if Settings.get_os() == Platform.WINDOWS or Settings.get_os() == Platform.LINUX:
            click(NavBar.HAMBURGER_MENU.target_offset(-170, 15))
            type(Key.ENTER)
        else:
            click(accept_risk)

        expected = region.exists(default_status, 10)
        assert_true(self, expected, 'The \'about:config\' page successfully loaded and default status is correct.')

        paste('keyword.enabled')
        type(Key.ENTER)

        expected = region.exists(default_status, 10)
        assert_true(self, expected, 'The \'keyword.enabled\' preference has status \'default\' by default.')

        expected = region.exists(true_value, 10)
        assert_true(self, expected, 'The \'keyword.enabled\' preference has value \'true\' by default.')

        double_click(default_status)

        expected = region.exists(modified_status, 10)
        assert_true(self, expected,
                    'The \'keyword.enabled\' preference has status \'modified\' after the preference has changed.')

        expected = region.exists(false_value, 10)
        assert_true(self, expected,
                    'The \'keyword.enabled\' preference has value \'false\' after the preference has changed.')

        select_location_bar()
        paste('amaz')

        expected = region.exists(search_with_url_autocomplete, 10)
        assert_true(self, expected, 'Search is performed with url autocomplete for pages where you\'\ve been before.')

        type(Key.ENTER)

        expected = exists(amazon_logo, 10)
        assert_true(self, expected, 'Page successfully loaded, amazon logo found.')

        # Perform a search using the same engine as the one used above.
        select_location_bar()
        paste('test')

        expected = region.exists(google_one_off_button, 10)
        assert_true(self, expected, 'The \'Google\' one-off button found.')

        click(google_one_off_button)
        time.sleep(DEFAULT_UI_DELAY_LONG)

        expected = region.exists(google_search_results, 10)
        assert_true(self, expected, 'Google search results are displayed.')
