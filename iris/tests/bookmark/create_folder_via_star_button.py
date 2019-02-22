# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Create a new folder using star-shaped button'
        self.test_case_id = '163404'
        self.test_suite_id = '2525' 
        self.locales = ['en-US']

    def run(self):
        bookmark_button_pattern = LocationBar.STAR_BUTTON_UNSTARRED
        other_bookmarks_folder_pattern = Bookmarks.StarDialog.PANEL_FOLDER_DEFAULT_OPTION
        choose_option_pattern = Bookmarks.StarDialog.PANEL_OPTION_CHOOSE
        bookmarks_toolbar_option_pattern = Library.BOOKMARKS_TOOLBAR
        new_folder_button_pattern = Bookmarks.StarDialog.NEW_FOLDER
        new_folder_created_pattern = Bookmarks.StarDialog.NEW_FOLDER_CREATED
        done_button_pattern = Bookmarks.StarDialog.DONE
        bookmark_folder_pattern = Pattern('moz_bookmark_folder.png').similar(0.7)

        if Settings.get_os() == Platform.LINUX:
            new_folder_created_pattern = Pattern('new_folder_created.png')

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        mozilla_page_assert = exists(LocalWeb.MOZILLA_LOGO, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, mozilla_page_assert, 'Test page loaded successfully.')

        bookmark_button_assert = exists(bookmark_button_pattern, DEFAULT_FIREFOX_TIMEOUT)        
        assert_true(self, bookmark_button_assert, 'Bookmark button present.')
        click(bookmark_button_pattern)

        other_bookmarks_folder_assert = exists(other_bookmarks_folder_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, other_bookmarks_folder_assert, 'Other bookmarks folder option present.')
        click(other_bookmarks_folder_pattern)

        choose_option_assert = exists(choose_option_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, choose_option_assert, 'Choose option present.')
        click(choose_option_pattern);

        bookmarks_toolbar_option_assert = exists(bookmarks_toolbar_option_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, bookmarks_toolbar_option_assert, 'Bookmarks toolbar option present.')
        click(bookmarks_toolbar_option_pattern)

        new_folder_button_assert = exists(new_folder_button_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, new_folder_button_assert, 'New folder button present.')
        click(new_folder_button_pattern)

        new_folder_created_assert = exists(new_folder_created_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, new_folder_created_assert, 'New folder created.')
        paste('moz_bookmark')

        done_button_assert = exists(done_button_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, done_button_assert, 'Done button present.')
        click(done_button_pattern)

        bookmark_folder_assert = exists(bookmark_folder_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, bookmark_folder_assert, 'Bookmark folder created successfully.')      
