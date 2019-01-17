# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This test case opens an URL in a new tab when the \'browser.search.openintab\' preference is ' \
                    'set to true.'
        self.test_case_id = '117527'
        self.test_suite_id = '1902'
        self.locales = ['en-US']

    def run(self):
        default_status_pattern = Pattern('default_status.png')
        modified_status_pattern = Pattern('modified_status.png')
        true_value_highlight_pattern = Pattern('true_value_highlight.png')
        false_value_no_highlight_pattern = Pattern('false_value_no_highlight.png')
        accept_risk_pattern = Pattern('accept_risk.png')
        url = LocalWeb.FIREFOX_TEST_SITE
        search_settings_pattern = Pattern('search_settings.png')

        region = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)

        navigate('about:config')
        expected = exists(accept_risk_pattern, 10)
        assert_true(self, expected, 'Need to accept the risks before continue to next step.')
        click(accept_risk_pattern)

        expected = region.exists(default_status_pattern, 10)
        assert_true(self, expected, 'The \'about:config\' page successfully loaded and default status is correct.')

        paste('browser.search.openintab')
        type(Key.ENTER)

        expected = region.exists(default_status_pattern, 10)
        assert_true(self, expected, 'The \'browser.search.openintab\' preference has status \'default\' by default.')

        expected = region.exists(false_value_no_highlight_pattern, 10)
        assert_true(self, expected, 'The \'browser.search.openintab\' preference has value \'false\' by default.')

        double_click(default_status_pattern)

        expected = region.exists(modified_status_pattern, 10)
        assert_true(self, expected, 'The \'browser.search.openintab\' preference has status \'modified\' after the '
                                    'preference has changed.')

        expected = region.exists(true_value_highlight_pattern, 10)
        assert_true(self, expected, 'The \'browser.search.openintab\' preference has value \'true\' after the '
                                    'preference has changed.')

        select_location_bar()
        paste('about:newtab')
        type(Key.ENTER)

        expected = region.exists(search_settings_pattern, 10)
        assert_true(self, expected, 'The \'about:newtab\' page successfully loaded.')

        select_location_bar()
        paste(url)
        type(Key.ENTER)

        # Link is opened in the same tab.
        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')
