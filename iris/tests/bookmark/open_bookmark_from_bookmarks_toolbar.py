# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Bookmarks can be opened from Bookmarks Toolbar.'
        self.test_case_id = '165206'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        getting_started_bookmark_pattern = Pattern('getting_started_in_toolbar.png')
        get_started_tab_pattern = Pattern('get_started_tab.png')

        open_bookmarks_toolbar()

        getting_started_bookmark_exists = exists(getting_started_bookmark_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, getting_started_bookmark_exists, 'Bookmarks Toolbar enabled. Getting started bookmark exists')

        click(getting_started_bookmark_pattern)

        get_started_page_opened = exists(get_started_tab_pattern, Settings.HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, get_started_page_opened, 'Get started page successfully opened')
