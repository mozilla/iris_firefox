# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='The removal of a bookmark can be undone.',
        locale=['en-US'],
        test_case_id='4156',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS,
        blocked_by={'id': '1385754', 'platform': OSPlatform.ALL}
    )
    def run(self, firefox):
        moz_draggable_pattern = Pattern('moz_sidebar_bookmark.png')
        drag_area_pattern = Pattern('drag_area.png')
        dragged_bookmark_pattern = Pattern('moz_toolbar_dragged_bookmark.png')
        delete = Pattern('delete_bookmark.png')
        view_bookmarks_toolbar_pattern = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_TOOLBAR

        navigate('about:blank')

        access_bookmarking_tools(view_bookmarks_toolbar_pattern)

        bookmarks_sidebar('open')

        paste('mozilla')

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        drag_drop(moz_draggable_pattern, drag_area_pattern, duration=0.5)

        bookmark_drag_assert = exists(dragged_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmark_drag_assert is True, 'Moz Bookmark was dragged successfully.'

        bookmarks_sidebar('close')

        right_click(dragged_bookmark_pattern)

        click(delete)

        try:
            deleted_bookmark_assert = wait_vanish(dragged_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            assert deleted_bookmark_assert is True, 'Moz bookmarks was successfully deleted.'
        except FindError:
            raise FindError('Moz bookmarks was not deleted')

        edit_undo()

        undo_bookmark_removal_assert = exists(dragged_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert undo_bookmark_removal_assert is True, 'The removal bookmark action has been successfully undone.'
