# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Add a new folder from Library'
        self.test_case_id = '169262'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        iris_new_folder_pattern = Pattern('iris_new_folder.png')
        if Settings.is_linux():
            new_folder_bookmark_bookmark = Pattern('new_folder_bookmark.png')

        open_library()

        library_opened = exists(Library.TITLE, Settings.FIREFOX_TIMEOUT)
        assert_true(self, library_opened, 'Library opened')

        other_bookmarks_folder_exists = exists(Library.OTHER_BOOKMARKS)
        assert_true(self, other_bookmarks_folder_exists, 'Other Bookmarks folder exists')

        other_bookmarks_width, other_bookmarks_height = Library.OTHER_BOOKMARKS.get_size()
        location_for_right_click = find(Library.OTHER_BOOKMARKS).right(other_bookmarks_width * 2)

        right_click(location_for_right_click)

        new_bookmark_option_exists = exists(Library.Organize.NEW_FOLDER)
        assert_true(self, new_bookmark_option_exists, 'New Folder option exists')

        click(Library.Organize.NEW_FOLDER)

        if Settings.is_linux():
            new_bookmark_window_opened = exists(new_folder_bookmark_bookmark)
            assert_true(self, new_bookmark_window_opened, 'New Folder window is displayed')
        else:
            new_bookmark_window_opened = exists(Bookmarks.StarDialog.NEW_FOLDER_CREATED)
            assert_true(self, new_bookmark_window_opened, 'New Folder window is displayed')

        paste('Iris New Folder')

        type(Key.ENTER)

        bookmark_exists = exists(iris_new_folder_pattern)
        assert_true(self, bookmark_exists, 'The New Folder is added in the selected section')

        click(Library.TITLE)

        close_window_control('auxiliary')
