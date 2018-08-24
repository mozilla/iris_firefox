# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'Bookmarks can be opened from Bookmarks Toolbar.'
        self.test_case_id = '4093'
        self.test_suite_id = '75'

    def setup(self):
        """Test case setup

        This overrides the setup method in the BaseTest class, so that it can use a brand new profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        moz_draggable_pattern = Pattern('moz_sidebar_bookmark.png')
        drag_area_pattern = Pattern('drag_area.png')
        dragged_bookmark_pattern = Pattern('moz_toolbar_dragged_bookmark.png')
        view_bookmarks_toolbar_pattern = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_TOOLBAR

        navigate('about:blank')

        access_bookmarking_tools(view_bookmarks_toolbar_pattern)

        bookmarks_sidebar('open')

        paste('mozilla')

        drag_drop(moz_draggable_pattern, drag_area_pattern, 0.5)

        bookmark_drag_assert = exists(dragged_bookmark_pattern, 10)
        assert_true(self, bookmark_drag_assert, 'Moz Bookmark was dragged successfully.')

        bookmarks_sidebar('close')

        click(dragged_bookmark_pattern)

        mozilla_page_assert = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, mozilla_page_assert,
                    'Moz bookmark has been successfully accessed from the Bookmarks Toolbar.')
