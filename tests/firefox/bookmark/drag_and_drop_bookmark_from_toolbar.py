# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Drag and drop a bookmark from \'Bookmark Toolbar\'',
        locale=['en-US'],
        test_case_id='164377',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        pocket_logo_pattern = LocalWeb.POCKET_LOGO
        most_visited_toolbar_bookmarks_folder_pattern = Pattern('drag_area.png')
        pocket_bookmark_pattern = Pattern('pocket_most_visited.png')

        open_bookmarks_toolbar()

        bookmarks_folder_available_in_toolbar = exists(most_visited_toolbar_bookmarks_folder_pattern,
                                                       FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmarks_folder_available_in_toolbar is True, 'The \'Bookmarks Toolbar\' is enabled.'

        click(most_visited_toolbar_bookmarks_folder_pattern)

        bookmark_available_in_folder = exists(pocket_bookmark_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmark_available_in_folder is True, '\'Pocket\' bookmark is displayed in \'Most visited\' bookmarks ' \
                                                     'folder in toolbar'

        drop_location = Location(Screen.SCREEN_WIDTH/2, Screen.SCREEN_HEIGHT/2)

        drag_drop(pocket_bookmark_pattern, drop_location, duration=3)

        bookmarked_website_loaded = exists(pocket_logo_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert bookmarked_website_loaded is True, 'The selected website is correctly opened.'
