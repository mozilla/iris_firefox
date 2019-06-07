# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='The Copy context menu option works properly.',
        locale=['en-US'],
        test_case_id='168934',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        toolbar_bookmark_pattern = Pattern('moz_toolbar_dragged_bookmark.png')
        close_sidebar_search_pattern = Pattern('close_sidebar_search.png')
        moz_sidebar_bookmark = Pattern('moz_sidebar_bookmark.png')
        drag_area = Pattern('drag_area.png')
        moz_location_changed = Pattern('moz_sidebar_bookmark_location_changed.png').similar(0.6)
        bookmarks_sidebar_menu_pattern = SidebarBookmarks.BOOKMARKS_MENU
        bookmarks_sidebar_menu_selected_pattern = SidebarBookmarks.BOOKMARKS_MENU_SELECTED
        view_bookmarks_toolbar_pattern = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_TOOLBAR
        paste_option_pattern = Pattern('paste_option.png')
        copy_option_pattern = Pattern('copy_option.png')

        navigate('about:blank')

        access_bookmarking_tools(view_bookmarks_toolbar_pattern)

        try:
            wait(SidebarBookmarks.BookmarksToolbar.MOST_VISITED, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('Toolbar has been activated.')
        except FindError:
            raise FindError('Toolbar can not be activated, aborting.')

        bookmarks_sidebar('open')

        paste('mozilla')

        sidebar_bookmark_assert = exists(moz_sidebar_bookmark, FirefoxSettings.FIREFOX_TIMEOUT)
        assert sidebar_bookmark_assert is True, 'Moz Bookmark is present inside the sidebar.'

        drag_drop(moz_sidebar_bookmark, drag_area, duration=0.5)

        toolbar_bookmark_assert = exists(toolbar_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert toolbar_bookmark_assert is True, 'Moz bookmark is present in the Bookmarks Toolbar.'

        right_click(toolbar_bookmark_pattern)

        click(copy_option_pattern)

        bookmarks_sidebar('close')

        bookmarks_sidebar('open')

        # try:
        #     wait(close_sidebar_search_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        #     logger.debug('Close button is present.')
        #     click(close_sidebar_search_pattern)
        # except FindError:
        #     raise FindError('Can\'t find the close button.')

        try:
            wait(bookmarks_sidebar_menu_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('Bookmarks sidebar menu is present.')
            click(bookmarks_sidebar_menu_pattern)
        except FindError:
            raise FindError('Can\'t find the Bookmarks sidebar menu.')

        right_click(bookmarks_sidebar_menu_selected_pattern)

        click(paste_option_pattern)

        pasted_bookmark_assertion = exists(moz_location_changed, FirefoxSettings.FIREFOX_TIMEOUT)
        assert pasted_bookmark_assertion is True, 'Moz Bookmark has been moved to a different directory, ' \
                                                  'copy option works as expected.'
