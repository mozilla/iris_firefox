# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Create "New Folder..." from "Bookmarks Toolbar"',
        locale=['en-US'],
        test_case_id='171637',
        test_suite_id='2525'
    )
    def run(self, firefox):
        folder_in_bookmarks_pattern = Pattern('folder_in_bookmarks_toolbar.png')
        mozilla_bookmark_icon_pattern = Pattern('mozilla_bookmark_icon.png')
        if OSHelper.is_linux():
            new_folder_window_pattern = Pattern('new_folder_bookmark.png')

        home_button_displayed = exists(NavBar.HOME_BUTTON)
        assert home_button_displayed is True, 'Home button displayed'

        open_bookmarks_toolbar()

        home_button_location = find(NavBar.HOME_BUTTON)
        proper_mozilla_bookmark_icon_region = Region(0, home_button_location.y, Screen.SCREEN_WIDTH,
                                                     Screen.SCREEN_HEIGHT/5)

        mozilla_bookmark_icon = exists(mozilla_bookmark_icon_pattern, region=proper_mozilla_bookmark_icon_region)
        assert mozilla_bookmark_icon is True, 'Mozilla bookmark icon displayed'

        right_click(mozilla_bookmark_icon_pattern)

        #  select Create new folder
        type('f')
        type(Key.ENTER)

        if OSHelper.is_linux():
            new_bookmark_window_opened = exists(new_folder_window_pattern)
            assert new_bookmark_window_opened is True, 'New Folder window is displayed'
        else:
            new_bookmark_window_opened = exists(Bookmarks.StarDialog.NEW_FOLDER_CREATED)
            assert new_bookmark_window_opened is True, 'New Folder window is displayed'

        type(Key.ENTER)

        folder_created_in_bookmarks = exists(folder_in_bookmarks_pattern)
        assert folder_created_in_bookmarks is True, 'The New Folder is correctly created in the Bookmarks ' \
                                                    'Toolbar menu.'
