# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This test case checks the position of the bookmark drop down for a highlighted link.'
        self.test_case_id = '117526'
        self.test_suite_id = '1902'
        self.locales = ['en-US']

    def run(self):
        url = LocalWeb.FIREFOX_TEST_SITE
        bookmark_button_pattern = LocationBar.STAR_BUTTON_UNSTARRED
        bookmark_drop_down_under_bookmark_icon_pattern = Pattern('bookmark_drop_down_under_bookmark_icon.png')

        navigate(url)
        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        select_location_bar()

        click(bookmark_button_pattern)
        expected = exists(bookmark_drop_down_under_bookmark_icon_pattern, 10)
        assert_true(self, expected, 'The bookmark drop down is displayed under the bookmark icon.')
