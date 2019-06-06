# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bookmarks can be opened from Bookmarks Toolbar.',
        locale=['en-US'],
        test_case_id='165206',
        test_suite_id='2525',
    )
    def run(self, firefox):
        getting_started_bookmark_pattern = Pattern('getting_started_in_toolbar.png')
        get_started_tab_pattern = Pattern('get_started_tab.png')

        open_bookmarks_toolbar()

        getting_started_bookmark_exists = exists(getting_started_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert getting_started_bookmark_exists is True, 'Bookmarks Toolbar enabled. Getting started bookmark exists'

        click(getting_started_bookmark_pattern)

        get_started_page_opened = exists(get_started_tab_pattern, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT)
        assert get_started_page_opened is True, 'Get started page successfully opened'
