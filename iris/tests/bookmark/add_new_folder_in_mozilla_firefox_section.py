# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Add a new Folder in \'Mozilla Firefox\' section '
        self.test_case_id = '163374'
        self.test_suite_id = '2525'
        self.locale = ['en-US']
        self.exclude = [Platform.MAC]

    def run(self):
        firefox_menu_bookmarks_pattern = Pattern('firefox_menu_bookmarks.png')
        mozilla_firefox_predefined_bookmarks_pattern = Pattern('mozilla_firefox_predefined_bookmarks.png')
        mozilla_firefox_bookmarks_folder_pattern = Pattern('mozilla_firefox_bookmarks_folder.png')
        mozilla_about_us_bookmark_pattern = Pattern('mozilla_about_us_bookmark.png')
        iris_new_folder_pattern = Pattern('ff_menu_iris_new_folder.png')
        if Settings.is_linux():
            new_folder_window_pattern = Pattern('new_folder_window.png')
        else:
            new_folder_window_pattern = Bookmarks.StarDialog.NEW_FOLDER_CREATED

        open_firefox_menu()

        firefox_menu_bookmarks_exists = exists(firefox_menu_bookmarks_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, firefox_menu_bookmarks_exists, 'Firefox menu > Bookmarks exists')

        click(firefox_menu_bookmarks_pattern)

        mozilla_firefox_bookmarks_folder_exists = exists(mozilla_firefox_bookmarks_folder_pattern,
                                                         Settings.FIREFOX_TIMEOUT)
        assert_true(self, mozilla_firefox_bookmarks_folder_exists, 'Firefox menu > Bookmarks > Mozilla Firefox '
                                                                   'bookmarks folder exists')
        click(mozilla_firefox_bookmarks_folder_pattern)

        mozilla_firefox_predefined_bookmarks_exists = exists(mozilla_firefox_predefined_bookmarks_pattern,
                                                             Settings.FIREFOX_TIMEOUT)
        assert_true(self, mozilla_firefox_predefined_bookmarks_exists, 'Predefined Mozilla Firefox related bookmarks '
                                                                       'displayed')

        right_click(mozilla_about_us_bookmark_pattern)

        new_folder_option_exists = exists(Library.Organize.NEW_FOLDER, Settings.FIREFOX_TIMEOUT)
        assert_true(self, new_folder_option_exists, 'New Folder option exists')

        click(Library.Organize.NEW_FOLDER)

        new_folder_window_opened = exists(new_folder_window_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, new_folder_window_opened, 'New Folder window is displayed')

        paste('Iris New Folder')
        type(Key.ENTER)

        open_firefox_menu()

        firefox_menu_bookmarks_second_exists = exists(firefox_menu_bookmarks_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, firefox_menu_bookmarks_second_exists, 'Firefox menu > Bookmarks exists')

        click(firefox_menu_bookmarks_pattern)

        mozilla_firefox_bookmarks_folder_second_exists = exists(mozilla_firefox_bookmarks_folder_pattern,
                                                                Settings.FIREFOX_TIMEOUT)
        assert_true(self, mozilla_firefox_bookmarks_folder_second_exists, 'Firefox menu > Bookmarks > Mozilla Firefox '
                                                                          'bookmarks folder exists')
        click(mozilla_firefox_bookmarks_folder_pattern)

        folder_exists = exists(iris_new_folder_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, folder_exists, 'A new folder is added in Mozilla Firefox section.')

        restore_firefox_focus()
