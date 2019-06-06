# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Change the elements order in \'Bookmarks Toolbar\' with drag & drop.',
        locale=['en-US'],
        test_case_id='164378',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        bookmarks_toolbar_menu_option_pattern = Pattern('bookmarks_toolbar_menu_option.png')
        iris_tab_pattern = Pattern('iris_tab.png')
        most_visited_toolbar_bookmarks_folder_pattern = Pattern('drag_area.png')
        getting_started_toolbar_bookmark_pattern = Pattern('toolbar_bookmark_icon.png')
        toolbar_bookmarks_reordered_pattern = Pattern('toolbar_bookmarks_reordered.png')

        open_bookmarks_toolbar()

        bookmarks_folder_available_in_toolbar = exists(most_visited_toolbar_bookmarks_folder_pattern,
                                                       FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmarks_folder_available_in_toolbar is True, 'The \'Bookmarks Toolbar\' is enabled.'

        area_to_drop = find(most_visited_toolbar_bookmarks_folder_pattern)
        area_to_drop.x -= 1

        drag_drop(getting_started_toolbar_bookmark_pattern, area_to_drop)

        bookmarks_reordered = exists(toolbar_bookmarks_reordered_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmarks_reordered is True, 'The position of the selected bookmark is changed as expected.'
