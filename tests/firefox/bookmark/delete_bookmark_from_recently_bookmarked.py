# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Delete a bookmark from the Recently Bookmarked section',
        locale=['en-US'],
        test_case_id='171647',
        test_suite_id='2525'
    )
    def run(self, firefox):
        getting_started_bookmark_pattern = Pattern('getting_started_bookmark.png')
        delete_bookmark_button_pattern = Pattern('delete_bookmark.png')

        click(NavBar.LIBRARY_MENU)

        bookmark_options_exists = exists(LibraryMenu.BOOKMARKS_OPTION)
        assert bookmark_options_exists is True, 'Bookmark option is on display'

        click(LibraryMenu.BOOKMARKS_OPTION)

        bookmark_menu_exists = exists(getting_started_bookmark_pattern)
        assert bookmark_menu_exists is True, 'The Bookmarks menu is correctly displayed'

        right_click(getting_started_bookmark_pattern)

        delete_bookmark_button_exists = exists(delete_bookmark_button_pattern)
        assert delete_bookmark_button_exists is True, 'Delete button is displayed'

        click(delete_bookmark_button_pattern)

        try:
            website_bookmark_not_exists = wait_vanish(getting_started_bookmark_pattern)
            assert website_bookmark_not_exists is True, 'The selected website is correctly deleted.'
        except FindError:
            raise FindError('The selected website is not deleted')
