# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Copy the history menu and paste it into the Bookmark toolbar.',
        locale=['en-US'],
        test_case_id='174031',
        test_suite_id='2000',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        show_all_history_pattern = History.HistoryMenu.SHOW_ALL_HISTORY
        view_bookmarks_toolbar = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_TOOLBAR
        bookmarks_toolbar_most_visited_pattern = SidebarBookmarks.BookmarksToolbar.MOST_VISITED
        library_pattern = Library.TITLE
        history_pattern = Library.HISTORY
        copy_pattern = Pattern('copy.png')
        paste_pattern = Pattern('paste.png')
        history_bookmarks_toolbar_pattern = Pattern('history_bookmarks_toolbar.png')

        # Open the Bookmarks toolbar.
        access_bookmarking_tools(view_bookmarks_toolbar)

        expected = exists(bookmarks_toolbar_most_visited_pattern, 10)
        assert expected, 'Bookmarks Toolbar has been activated.'

        # Check that the Library window is displayed properly.
        open_library_menu('History')

        try:
            wait(show_all_history_pattern, 10)
            logger.debug('Show All History option found.')
            click(show_all_history_pattern)
        except FindError:
            raise FindError('Show All History option is not present on the page, aborting.')

        expected = exists(library_pattern, 10)
        assert expected, '\"Library\" window was displayed properly.'

        # Copy the history.
        expected = exists(history_pattern, 10)
        assert expected, 'History item was found.'

        right_click(history_pattern)

        time.sleep(Settings.DEFAULT_UI_DELAY)

        expected = exists(copy_pattern, 10)
        assert expected, 'Copy option was found.'

        click(copy_pattern)

        time.sleep(Settings.DEFAULT_UI_DELAY)

        click_window_control('close')

        time.sleep(Settings.DEFAULT_UI_DELAY)

        # Paste the history.
        right_click(bookmarks_toolbar_most_visited_pattern)

        expected = exists(paste_pattern, 10)
        assert expected, 'Paste option was found.'

        time.sleep(Settings.DEFAULT_UI_DELAY)
        click(paste_pattern)

        # Check that the history was copied.
        time.sleep(Settings.DEFAULT_UI_DELAY)
        region = Screen().new_region(0, 0, Screen.SCREEN_WIDTH / 2, Screen.SCREEN_HEIGHT / 2)

        expected = region.exists(history_bookmarks_toolbar_pattern, 10)
        assert expected, 'History was successfully copied.'
