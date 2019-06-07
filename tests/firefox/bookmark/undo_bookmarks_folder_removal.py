# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='The removal of a bookmarks folder can be undone.',
        locale=['en-US'],
        test_case_id='4157',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS,
        blocked_by={'id': '1385754', 'platform': OSPlatform.ALL}
    )
    def run(self, firefox):
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

        click(new_folder)

        new_folder_window_assert = exists(add_button, FirefoxSettings.FIREFOX_TIMEOUT)
        assert new_folder_window_assert is True, 'New Folder window is present on the page.'

        paste('moz_bookmark')

        click(add_button)

        moz_bookmark_folder_assert = exists(moz_bookmark, FirefoxSettings.FIREFOX_TIMEOUT)
        assert moz_bookmark_folder_assert is True, 'Moz Bookmark folder is present on the page.'

        bookmarks_sidebar('open')

        paste('mozilla')

        drag_drop(moz_draggable_pattern, moz_bookmark, duration=0.5)

        bookmark_drag_assert = exists(dragged_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmark_drag_assert is True, 'Moz Bookmark was dragged successfully inside the bookmark folder.'

        bookmarks_sidebar('close')

        right_click(moz_bookmark)

        click(delete)

        deleted_bookmark_assert = wait_vanish(moz_bookmark, FirefoxSettings.FIREFOX_TIMEOUT)
        assert deleted_bookmark_assert is True, 'Bookmark folder has been deleted.'

        edit_undo()

        undo_bookmarks_folder_removal_assert = exists(moz_bookmark, FirefoxSettings.FIREFOX_TIMEOUT)
        assert undo_bookmarks_folder_removal_assert is True, 'The removal of bookmarks folder action has' \
                                                             ' been successfully undone.'
