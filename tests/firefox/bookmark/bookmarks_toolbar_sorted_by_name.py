# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='The items from the Bookmarks Toolbar can be sorted by name.',
        locale=['en-US'],
        test_case_id='4161',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        moz_draggable_pattern = Pattern('moz_sidebar_bookmark.png')
        drag_area_pattern = Pattern('drag_area.png')
        dragged_bookmark_pattern = Pattern('moz_toolbar_dragged_bookmark.png')
        firefox_bookmark = Pattern('firefox_bookmark.png').similar(0.5)
        pocket_bookmark = Pattern('pocket_sidebar_bookmark.png')
        firefox_toolbar_bookmark = Pattern('firefox_toolbar_bookmark.png')
        pocket_toolbar_bookmark = Pattern('pocket_toolbar_bookmark.png')
        sort_by_name = Pattern('sort_by_name_option.png')
        toolbar_bookmarks_sorted_by_name = Pattern('toolbar_bookmarks_sorted_by_name.png')
        view_bookmarks_toolbar_pattern = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_TOOLBAR
        bookmarks_toolbar_menu = SidebarBookmarks.BOOKMARKS_TOOLBAR_MENU
        other_bookmarks_pattern = SidebarBookmarks.OTHER_BOOKMARKS

        navigate('about:blank')

        access_bookmarking_tools(view_bookmarks_toolbar_pattern)

        bookmarks_sidebar('open')

        click(other_bookmarks_pattern)

        try:
            wait(moz_draggable_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('Moz bookmark is present inside the Bookmarks Sidebar.')
            drag_drop(moz_draggable_pattern, drag_area_pattern, duration=0.5)
        except FindError:
            raise FindError('Moz bookmark is NOT present inside the Bookmarks Sidebar, aborting.')

        moz_bookmark_drag_assert = exists(dragged_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert moz_bookmark_drag_assert is True, 'Moz Bookmark was dragged successfully.'

        try:
            wait(firefox_bookmark, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('Firefox bookmark is present inside the Bookmarks Sidebar.')
            drag_drop(firefox_bookmark, drag_area_pattern, duration=0.5)
        except FindError:
            raise FindError('Firefox bookmark is NOT present inside the Bookmarks Sidebar, aborting.')

        firefox_bookmark_drag_assert = exists(firefox_toolbar_bookmark, FirefoxSettings.FIREFOX_TIMEOUT)
        assert firefox_bookmark_drag_assert is True, 'Firefox Bookmark was dragged successfully.'

        try:
            wait(pocket_bookmark, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('Pocket bookmark is present inside the Bookmarks Sidebar.')
            drag_drop(pocket_bookmark, drag_area_pattern, duration=0.5)
        except FindError:
            raise FindError('Pocket bookmark is NOT present inside the Bookmarks Sidebar, aborting.')

        pocket_bookmark_drag_assert = exists(pocket_toolbar_bookmark, FirefoxSettings.FIREFOX_TIMEOUT)
        assert pocket_bookmark_drag_assert is True, 'Pocket Bookmark was dragged successfully.'

        try:
            wait(bookmarks_toolbar_menu, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('Bookmarks Toolbar menu is present on the page.')
            right_click(bookmarks_toolbar_menu)
        except FindError:
            raise FindError('Bookmarks Toolbar menu is NOT present on the page.')

        try:
            wait(sort_by_name, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('Sort by name option is present on the page.')
            click(sort_by_name)
        except FindError:
            raise FindError('Sort by name option is NOT present on the page.')

        time.sleep(FirefoxSettings.FIREFOX_TIMEOUT/4)

        toolbar_bookmarks_sorted_by_name_assert = exists(toolbar_bookmarks_sorted_by_name.similar(0.87),
                                                         FirefoxSettings.FIREFOX_TIMEOUT)
        assert toolbar_bookmarks_sorted_by_name_assert is True, 'The items from the Bookmarks Toolbar has been ' \
                                                                'successfully sorted by name.'
