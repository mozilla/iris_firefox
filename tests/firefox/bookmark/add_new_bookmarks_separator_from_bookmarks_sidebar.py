# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Add a new bookmarks separator from Bookmarks Sidebar',
        locale=['en-US'],
        test_case_id='168932',
        test_suite_id='2525'
    )
    def run(self, firefox):
        separator_line_pattern = Pattern('separator.png')
        bookmark_site_pattern = Pattern('bookmark_site.png')
        mozilla_bookmark_pattern = Pattern('mozilla_bookmark.png')
        new_separator_pattern = Library.Organize.NEW_SEPARATOR

        if not OSHelper.is_mac():
            bookmark_menu_pattern = Library.BOOKMARKS_MENU
        else:
            bookmark_menu_pattern = Pattern('bookmarks_menu.png')

        bookmarks_sidebar('open')

        bookmark_menu_exists = exists(bookmark_menu_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmark_menu_exists is True, 'Bookmarks Sidebar is correctly displayed'

        click(bookmark_menu_pattern)

        mozilla_bookmark_exists = exists(mozilla_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_bookmark_exists is True, 'Mozilla bookmarks button exists'

        click(mozilla_bookmark_pattern)

        bookmark_site_exists = exists(bookmark_site_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmark_site_exists is True, 'Website bookmark exists'

        right_click(bookmark_site_pattern)

        new_separator_exists = exists(new_separator_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert new_separator_exists is True, 'Separator button exists'

        click(new_separator_pattern)

        separator_line_exists = exists(separator_line_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert separator_line_exists is True, 'A new separator is displayed above the selected bookmark.'
