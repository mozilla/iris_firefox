# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Open a bookmark from toolbar in a New Tab',
        locale=['en-US'],
        test_case_id='164364',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        most_visited_toolbar_bookmarks_folder_pattern = Pattern('drag_area.png')
        open_in_new_tab_option_pattern = Pattern('open_in_new_tab_option.png')
        pocket_bookmark_icon_pattern = Pattern('pocket_bookmark_icon.png')

        open_bookmarks_toolbar()

        bookmarks_folder_available_in_toolbar = exists(most_visited_toolbar_bookmarks_folder_pattern,
                                                       FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmarks_folder_available_in_toolbar is True, 'The \'Bookmarks Toolbar\' is enabled.'

        click(most_visited_toolbar_bookmarks_folder_pattern)

        pocket_bookmark_available = exists(pocket_bookmark_icon_pattern)
        assert pocket_bookmark_available is True, '\'Pocket\' bookmark is available in the \'Most visited\' ' \
                                                  'folder in toolbar'

        right_click(pocket_bookmark_icon_pattern)

        open_in_new_tab_option_available = exists(open_in_new_tab_option_pattern)
        assert open_in_new_tab_option_available is True, '\'Open in new tab\' option in available in context ' \
                                                         'menu after right-click at the bookmark in toolbar.'

        click(open_in_new_tab_option_pattern)

        website_opened_in_new_tab = exists(LocalWeb.POCKET_IMAGE, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert website_opened_in_new_tab is True, 'The selected website is opened in a new tab.'

        iris_tab_exists = exists(LocalWeb.IRIS_LOGO_INACTIVE_TAB, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert iris_tab_exists is True, '\'Iris\' tab is still displayed on the screen'
