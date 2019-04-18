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
        url = LocalWeb.FIREFOX_TEST_SITE
        search_settings_pattern = Pattern('search_settings.png')

        region = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)

        change_preference('browser.search.openintab', True)
        navigate('about:newtab')

        expected = region.exists(search_settings_pattern, 10)
        assert_true(self, expected, 'The \'about:newtab\' page successfully loaded.')

        expected = exists(Tabs.NEW_TAB_HIGHLIGHTED, 10)
        assert_true(self, expected, 'Tab information is correctly displayed.')

        select_location_bar()
        paste(url)
        type(Key.ENTER)

        # Link is opened in the same tab.
        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        expected = exists(Tabs.NEW_TAB_HIGHLIGHTED, 10)
        assert_false(self, expected, 'Link is opened in the same tab.')
