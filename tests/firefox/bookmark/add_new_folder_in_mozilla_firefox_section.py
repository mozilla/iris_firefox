# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Add a new Folder in \'Mozilla Firefox\' section',
        locale=['en-US'],
        test_case_id='163374',
        test_suite_id='2525',
        exclude=OSPlatform.MAC
    )
    def run(self, firefox):
        firefox_menu_bookmarks_pattern = Pattern('firefox_menu_bookmarks.png')
        mozilla_firefox_predefined_bookmarks_pattern = Pattern('mozilla_firefox_predefined_bookmarks.png')
        mozilla_firefox_bookmarks_folder_pattern = Pattern('mozilla_firefox_bookmarks_folder.png')
        mozilla_about_us_bookmark_pattern = Pattern('mozilla_about_us_bookmark.png')
        iris_new_folder_pattern = Pattern('ff_menu_iris_new_folder.png')
        if OSHelper.is_linux():
            new_folder_window_pattern = Pattern('new_folder_window.png')
        else:
            new_folder_window_pattern = Bookmarks.StarDialog.NEW_FOLDER_CREATED

        open_firefox_menu()

        firefox_menu_bookmarks_exists = exists(firefox_menu_bookmarks_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert firefox_menu_bookmarks_exists is True, 'Firefox menu > Bookmarks exists'

        click(firefox_menu_bookmarks_pattern)

        mozilla_firefox_bookmarks_folder_exists = exists(mozilla_firefox_bookmarks_folder_pattern,
                                                         FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_firefox_bookmarks_folder_exists is True, 'Firefox menu > Bookmarks > Mozilla Firefox ' \
                                                                'bookmarks folder exists'
        click(mozilla_firefox_bookmarks_folder_pattern)

        mozilla_firefox_predefined_bookmarks_exists = exists(mozilla_firefox_predefined_bookmarks_pattern,
                                                             FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_firefox_predefined_bookmarks_exists is True, 'Predefined Mozilla Firefox related bookmarks ' \
                                                                    'displayed'

        right_click(mozilla_about_us_bookmark_pattern)

        new_folder_option_exists = exists(Library.Organize.NEW_FOLDER, FirefoxSettings.FIREFOX_TIMEOUT)
        assert new_folder_option_exists is True, 'New Folder option exists'

        click(Library.Organize.NEW_FOLDER)

        new_folder_window_opened = exists(new_folder_window_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert new_folder_window_opened is True, 'New Folder window is displayed'

        paste('Iris New Folder')
        type(Key.ENTER)

        open_firefox_menu()

        firefox_menu_bookmarks_second_exists = exists(firefox_menu_bookmarks_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert firefox_menu_bookmarks_second_exists is True, 'Firefox menu > Bookmarks exists'

        click(firefox_menu_bookmarks_pattern)

        mozilla_firefox_bookmarks_folder_second_exists = exists(mozilla_firefox_bookmarks_folder_pattern,
                                                                FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_firefox_bookmarks_folder_second_exists is True, 'Firefox menu > Bookmarks > Mozilla Firefox ' \
                                                                       'bookmarks folder exists'
        click(mozilla_firefox_bookmarks_folder_pattern)

        folder_exists = exists(iris_new_folder_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert folder_exists is True, 'A new folder is added in Mozilla Firefox section.'

        restore_firefox_focus()
