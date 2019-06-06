# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bookmark folders can be copied via context menu.',
        locale=['en-US'],
        test_case_id='4151',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        moz_draggable_pattern = Pattern('moz_sidebar_bookmark.png')
        drag_area_pattern = Pattern('drag_area.png')
        dragged_bookmark_pattern = Pattern('dragged_to_folder.png')
        new_folder = Pattern('new_folder_option.png')
        add_button = Pattern('add_button.png')
        moz_bookmark = Pattern('moz_bookmark_folder.png')
        pasted_bookmark_folder = Pattern('pasted_bookmark_folder.png').similar(0.6)
        cut_option_pattern = Pattern('cut_option.png')
        paste_option_pattern = Pattern('paste_option.png')
        bookmarks_sidebar_menu_pattern = SidebarBookmarks.BOOKMARKS_MENU
        bookmarks_sidebar_menu_selected_pattern = SidebarBookmarks.BOOKMARKS_MENU_SELECTED
        view_bookmarks_toolbar_pattern = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_TOOLBAR

        navigate('about:blank')

        access_bookmarking_tools(view_bookmarks_toolbar_pattern)

        right_click(drag_area_pattern)

        click(new_folder)

        new_folder_window_assert = exists(add_button, FirefoxSettings.FIREFOX_TIMEOUT)
        assert new_folder_window_assert is True, 'New Folder window is present on the page.'

        paste('moz_bookmark')

        click(add_button)

        moz_bookmark_folder_assert = exists(moz_bookmark, FirefoxSettings.FIREFOX_TIMEOUT)
        assert moz_bookmark_folder_assert is True, 'Moz Bookmark folder is present on the page.'

        bookmarks_sidebar('open')

        paste('mozilla')

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        drag_drop(moz_draggable_pattern, moz_bookmark, duration=0.5)

        bookmark_drag_assert = exists(dragged_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmark_drag_assert is True, 'Moz Bookmark was dragged successfully inside the bookmark folder.'

        type(Key.ESC)

        bookmarks_sidebar('close')

        right_click(moz_bookmark)

        click(cut_option_pattern)

        bookmarks_sidebar('open')

        try:
            wait(bookmarks_sidebar_menu_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('Bookmarks sidebar menu is present.')
            click(bookmarks_sidebar_menu_pattern)
        except FindError:
            raise FindError('Can\'t find the Bookmarks sidebar menu.')

        right_click(bookmarks_sidebar_menu_selected_pattern)

        click(paste_option_pattern)

        pasted_bookmark_folder_assertion = exists(pasted_bookmark_folder, FirefoxSettings.FIREFOX_TIMEOUT)
        assert pasted_bookmark_folder_assertion is True, 'Moz Bookmark has been moved to a different directory,' \
                                                         ' cut option works as expected.'

        moz_bookmark_vanish_assert = wait_vanish(moz_bookmark.similar(0.9), FirefoxSettings.FIREFOX_TIMEOUT)
        assert moz_bookmark_vanish_assert is True, 'Moz bookmark folder has been successfully cut.'
