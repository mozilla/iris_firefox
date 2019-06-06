# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Open a bookmark in a New Private Window from Bookmarks Sidebar',
        locale=['en-US'],
        test_case_id='168929',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        bookmarks_sidebar_menu_header_pattern = SidebarBookmarks.BOOKMARKS_HEADER
        new_private_window_pattern = PrivateWindow.private_window_pattern
        firefox_sidebar_logo_pattern = Pattern('firefox_bookmark.png')
        open_in_new_window_option_pattern = Pattern('open_in_new_private_window.png')

        if OSHelper.is_mac():
            other_bookmarks_pattern = Pattern('other_bookmarks.png')
        else:
            other_bookmarks_pattern = Library.OTHER_BOOKMARKS

        bookmarks_sidebar('open')

        bookmarks_sidebar_menu_exists = exists(bookmarks_sidebar_menu_header_pattern,
                                               FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmarks_sidebar_menu_exists is True, 'Bookmarks Sidebar is correctly displayed.'

        other_bookmarks_exists = exists(other_bookmarks_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert other_bookmarks_exists is True, 'Other bookmarks exists'

        click(other_bookmarks_pattern)

        firefox_sidebar_logo_exists = exists(firefox_sidebar_logo_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert firefox_sidebar_logo_exists is True, 'Firefox bookmark exists'

        right_click(firefox_sidebar_logo_pattern)

        open_option_exists = exists(open_in_new_window_option_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert open_option_exists is True, 'Open in New Private Window option exists'

        click(open_in_new_window_option_pattern)

        firefox_full_logo_exists = exists(LocalWeb.FIREFOX_IMAGE, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert firefox_full_logo_exists is True, 'Firefox content exists'

        new_private_window_exists = exists(new_private_window_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert new_private_window_exists is True, 'The page is correctly opened in a new private window.'

        close_window()




