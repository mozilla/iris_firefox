# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Bug 1391166 - Reordering of Bookmarks via Drag&Drop is incorrect'
        self.test_case_id = '171598'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        library_mozilla_firefox_folder_pattern = Pattern('library_mozilla_firefox_folder.png')

        open_library()

        library_opened = exists(Library.TITLE, Settings.FIREFOX_TIMEOUT)
        assert_true(self, library_opened, 'Library is opened')

        maximize_window()

        bookmark_menu_folder_exists = exists(Library.BOOKMARKS_MENU)
        assert_true(self, bookmark_menu_folder_exists, 'bookmark_menu_folder_exists')

        click(Library.BOOKMARKS_MENU)

        mozilla_firefox_folder_exists = exists(library_mozilla_firefox_folder_pattern)
        assert_true(self, mozilla_firefox_folder_exists, 'mozilla_firefox_folder_exists')

