# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'The removal of a bookmarks folder can be undone.'
        self.test_case_id = '4157'
        self.test_suite_id = '2525'
        self.blocked_by = {'id': '1385754', 'platform': Platform.ALL}
        self.locales = ['en-US']

    def setup(self):
        """Test case setup

        Override the setup method to use a pre-canned bookmarks profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        moz_draggable_pattern = Pattern('moz_sidebar_bookmark.png')
        drag_area_pattern = Pattern('drag_area.png')
        dragged_bookmark_pattern = Pattern('dragged_to_folder.png')
        new_folder = Pattern('new_folder_option.png')
        add_button = Pattern('add_button.png')
        moz_bookmark = Pattern('moz_bookmark_folder.png')
        delete = Pattern('delete_bookmark.png')
        view_bookmarks_toolbar_pattern = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_TOOLBAR

        navigate('about:blank')

        access_bookmarking_tools(view_bookmarks_toolbar_pattern)

        right_click(drag_area_pattern)

        bookmark_options(new_folder)

        new_folder_window_assert = exists(add_button, 10)
        assert_true(self, new_folder_window_assert, 'New Folder window is present on the page.')

        paste('moz_bookmark')

        click(add_button)

        moz_bookmark_folder_assert = exists(moz_bookmark, 10)
        assert_true(self, moz_bookmark_folder_assert, 'Moz Bookmark folder is present on the page.')

        bookmarks_sidebar('open')

        paste('mozilla')

        drag_drop(moz_draggable_pattern, moz_bookmark, 0.5)

        bookmark_drag_assert = exists(dragged_bookmark_pattern, 10)
        assert_true(self, bookmark_drag_assert, 'Moz Bookmark was dragged successfully inside the bookmark folder.')

        click(Pattern('close_sidebar_search.png'))

        bookmarks_sidebar('close')

        right_click(moz_bookmark)

        bookmark_options(delete)

        deleted_bookmark_assert = wait_vanish(moz_bookmark, 10)
        assert_true(self, deleted_bookmark_assert, 'Bookmark folder has been deleted.')

        edit_undo()

        undo_bookmarks_folder_removal_assert = exists(moz_bookmark, 10)
        assert_true(self, undo_bookmarks_folder_removal_assert, 'The removal of bookmarks folder action has been '
                                                                'successfully undone.')
