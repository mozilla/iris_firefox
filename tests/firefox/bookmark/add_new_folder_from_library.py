# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Add a new folder from Library',
        locale=['en-US'],
        test_case_id='169262',
        test_suite_id='2525'
    )
    def run(self, firefox):
        iris_new_folder_pattern = Pattern('iris_new_folder.png')
        if OSHelper.is_linux():
            new_folder_bookmark_bookmark = Pattern('new_folder_bookmark.png')

        open_library()

        library_opened = exists(Library.TITLE, FirefoxSettings.FIREFOX_TIMEOUT)
        assert library_opened is True, 'Library opened'

        other_bookmarks_folder_exists = exists(Library.OTHER_BOOKMARKS)
        assert other_bookmarks_folder_exists is True, 'Other Bookmarks folder exists'

        other_bookmarks_width, other_bookmarks_height = Library.OTHER_BOOKMARKS.get_size()

        right_click(Library.OTHER_BOOKMARKS.target_offset(other_bookmarks_width * 2, 0))

        new_bookmark_option_exists = exists(Library.Organize.NEW_FOLDER)
        assert new_bookmark_option_exists is True, 'New Folder option exists'

        click(Library.Organize.NEW_FOLDER)

        if OSHelper.is_linux():
            new_bookmark_window_opened = exists(new_folder_bookmark_bookmark)
            assert new_bookmark_window_opened is True, 'New Folder window is displayed'
        else:
            new_bookmark_window_opened = exists(Bookmarks.StarDialog.NEW_FOLDER_CREATED)
            assert new_bookmark_window_opened is True, 'New Folder window is displayed'

        paste('Iris New Folder')

        type(Key.ENTER)

        bookmark_exists = exists(iris_new_folder_pattern)
        assert bookmark_exists is True, 'The New Folder is added in the selected section'

        click(Library.TITLE)

        close_window_control('auxiliary')
