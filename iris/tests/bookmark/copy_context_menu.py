# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'The Copy context menu option works properly.'
        self.test_case_id = '168934'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        """Test case setup

        Override the setup method to use a pre-canned bookmarks profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):

        toolbar_bookmark_pattern = Pattern('moz_toolbar_dragged_bookmark.png')
        close_sidebar_search_pattern = Pattern('close_sidebar_search.png')
        moz_sidebar_bookmark = Pattern('moz_sidebar_bookmark.png')
        drag_area = Pattern('drag_area.png')
        moz_location_changed = Pattern('moz_sidebar_bookmark_location_changed.png').similar(0.6)
        bookmarks_sidebar_menu_pattern = SidebarBookmarks.BOOKMARKS_MENU
        bookmarks_sidebar_menu_selected_pattern = SidebarBookmarks.BOOKMARKS_MENU_SELECTED
        view_bookmarks_toolbar_pattern = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_TOOLBAR

        navigate('about:blank')

        access_bookmarking_tools(view_bookmarks_toolbar_pattern)

        try:
            wait(SidebarBookmarks.BookmarksToolbar.MOST_VISITED, 10)
            logger.debug('Toolbar has been activated.')
        except FindError:
            raise FindError('Toolbar can not be activated, aborting.')

        bookmarks_sidebar('open')

        paste('mozilla')

        sidebar_bookmark_assert = exists(moz_sidebar_bookmark, 10)
        assert_true(self, sidebar_bookmark_assert, 'Moz Bookmark is present inside the sidebar.')

        drag_drop(moz_sidebar_bookmark, drag_area, 0.5)

        toolbar_bookmark_assert = exists(toolbar_bookmark_pattern, 10)
        assert_true(self, toolbar_bookmark_assert, 'Moz bookmark is present in the Bookmarks Toolbar.')

        right_click(toolbar_bookmark_pattern)

        bookmark_options(Pattern('copy_option.png'))

        try:
            wait(close_sidebar_search_pattern, 10)
            logger.debug('Close button is present.')
            click(close_sidebar_search_pattern)
        except FindError:
            raise FindError('Can\'t find the close button.')

        try:
            wait(bookmarks_sidebar_menu_pattern, 10)
            logger.debug('Bookmarks sidebar menu is present.')
            click(bookmarks_sidebar_menu_pattern)
        except FindError:
            raise FindError('Can\'t find the Bookmarks sidebar menu.')

        right_click(bookmarks_sidebar_menu_selected_pattern)

        bookmark_options(Pattern('paste_option.png'))

        pasted_bookmark_assertion = exists(moz_location_changed, 10)
        assert_true(self, pasted_bookmark_assertion,
                    'Moz Bookmark has been moved to a different directory, copy option works as expected.')
