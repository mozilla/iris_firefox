# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Delete items from \'Bookmarks Toolbar\'',
        locale=['en-US'],
        test_case_id='164373',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        getting_started_toolbar_bookmark_pattern = Pattern('toolbar_bookmark_icon.png')
        bookmark_delete_option = Pattern('delete_bookmark.png')

        open_bookmarks_toolbar()

        bookmarks_folder_available_in_toolbar = exists(getting_started_toolbar_bookmark_pattern)
        assert bookmarks_folder_available_in_toolbar is True, 'The \'Bookmarks Toolbar\' is enabled.'

        right_click(getting_started_toolbar_bookmark_pattern)

        delete_option_available = exists(bookmark_delete_option)
        assert delete_option_available is True, '\'Delete\' option in available in context menu after right-click ' \
                                                'at the bookmark in toolbar.'

        click(bookmark_delete_option)

        try:
            bookmark_deleted = wait_vanish(getting_started_toolbar_bookmark_pattern)
            assert bookmark_deleted is True, 'The bookmark is deleted from the \'Bookmarks Toolbar\' section.'
        except FindError:
            raise FindError(' The website is not deleted from the list.')
