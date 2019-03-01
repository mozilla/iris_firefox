# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'The removal of a bookmark can be undone.'
        self.test_case_id = '4156'
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
        dragged_bookmark_pattern = Pattern('moz_toolbar_dragged_bookmark.png')
        delete = Pattern('delete_bookmark.png')
        view_bookmarks_toolbar_pattern = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_TOOLBAR

        navigate('about:blank')

        access_bookmarking_tools(view_bookmarks_toolbar_pattern)

        bookmarks_sidebar('open')

        paste('mozilla')

        time.sleep(DEFAULT_UI_DELAY)

        drag_drop(moz_draggable_pattern, drag_area_pattern, 0.5)

        bookmark_drag_assert = exists(dragged_bookmark_pattern, 10)
        assert_true(self, bookmark_drag_assert, 'Moz Bookmark was dragged successfully.')

        bookmarks_sidebar('close')

        right_click(dragged_bookmark_pattern)

        bookmark_options(delete)

        deleted_bookmark_assert = wait_vanish(dragged_bookmark_pattern, 10)
        assert_true(self, deleted_bookmark_assert, 'Moz bookmarks was successfully deleted.')

        edit_undo()

        undo_bookmark_removal_assert = exists(dragged_bookmark_pattern, 10)
        assert_true(self, undo_bookmark_removal_assert, 'The removal bookmark action has been successfully undone.')
