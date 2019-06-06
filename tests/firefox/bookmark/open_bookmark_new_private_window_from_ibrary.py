# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Open a bookmark in a New Private Window from Library',
        locale=['en-US'],
        test_case_id='169260',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        open_new_private_window_pattern = Pattern('open_in_private_window.png')
        bookmark_menu_pattern = Library.BOOKMARKS_MENU
        private_window_pattern = PrivateWindow.private_window_pattern

        if not OSHelper.is_mac():
            mozilla_bookmark_pattern = Pattern('mozilla_bookmark.png')
            bookmark_site_pattern = Pattern('bookmark_site.png')
        else:
            mozilla_bookmark_pattern = Pattern('mozilla_firefox_bookmark.png')
            bookmark_site_pattern = Pattern('website_bookmark_from_library.png')

        open_library()

        library_is_displayed = exists(bookmark_menu_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert library_is_displayed is True, 'Library is correctly open'

        click(bookmark_menu_pattern)

        mozilla_bookmark_exists = exists(mozilla_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_bookmark_exists is True, 'Mozilla bookmark exists'

        double_click(mozilla_bookmark_pattern)

        bookmark_site_exists = exists(bookmark_site_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmark_site_exists is True, 'Website bookmark exists'

        right_click(bookmark_site_pattern)

        open_new_private_window_exists = exists(open_new_private_window_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert open_new_private_window_exists is True, 'Open new private window button exists'

        click(open_new_private_window_pattern)

        private_window_exists = exists(private_window_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert private_window_exists is True, 'The selected bookmark page is opened in a new private window.'

        close_window()
        close_window_control('auxiliary')
