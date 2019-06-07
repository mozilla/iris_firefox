# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Change the bookmarks order by drag&drop in \'Bookmarks Sidebar\'',
        locale=['en-US'],
        test_case_id='168938',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        reordered_sidebar_bookmarks_pattern = Pattern('sidebar_bookmarks_reordered.png')
        pocket_bookmark_pattern = Pattern('pocket_sidebar_bookmark.png')
        mozilla_bookmark_pattern = Pattern('moz_sidebar_bookmark.png')
        other_bookmarks_pattern = Pattern('other_bookmarks_sidebar.png')

        bookmarks_sidebar('open')

        sidebar_opened = exists(other_bookmarks_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert sidebar_opened is True, '\'Bookmarks Sidebar\' is correctly displayed.'

        click(other_bookmarks_pattern)

        pocket_bookmark_available = exists(pocket_bookmark_pattern)
        assert pocket_bookmark_available is True, '\'Pocket\' bookmark is available in \'Other bookmarks\' ' \
                                                  'folder in \'Bookmarks sidebar\''

        mozilla_bookmark_available = exists(mozilla_bookmark_pattern)
        assert mozilla_bookmark_available is True, '\'Mozilla\' bookmark is available in \'Other bookmarks\' ' \
                                                   'folder in \'Bookmarks sidebar\''

        mozilla_bookmark_location = find(mozilla_bookmark_pattern)

        drag_drop(pocket_bookmark_pattern, mozilla_bookmark_location)

        bookmarks_not_reordered = exists(reordered_sidebar_bookmarks_pattern)
        assert bookmarks_not_reordered is True, 'The bookmarks order is correctly modified.'
