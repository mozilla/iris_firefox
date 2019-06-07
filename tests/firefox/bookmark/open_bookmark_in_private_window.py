# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Open a bookmark in a New Private Window',
        locale=['en-US'],
        test_case_id='164366',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        open_in_private_window_option_pattern = Pattern('open_in_private_window_option.png')
        pocket_bookmark_icon_pattern = Pattern('pocket_bookmark_icon.png')
        most_visited_toolbar_bookmark_pattern = Pattern('drag_area.png')

        open_bookmarks_toolbar()

        bookmark_available_in_toolbar = exists(most_visited_toolbar_bookmark_pattern,
                                               FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmark_available_in_toolbar is True, 'The \'Bookmarks Toolbar\' is enabled.'

        click(most_visited_toolbar_bookmark_pattern)

        pocket_bookmark_available = exists(pocket_bookmark_icon_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert pocket_bookmark_available is True, '\'Pocket\' bookmark is available in \'Most visited\'' \
                                                  ' folder in toolbar'

        right_click(pocket_bookmark_icon_pattern)

        open_in_private_window_option_available = exists(open_in_private_window_option_pattern,
                                                         FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert open_in_private_window_option_available is True, '\'Open in Private window\' option is available in ' \
                                                                'context menu after right-click at the bookmark'

        click(open_in_private_window_option_pattern)

        bookmark_opened_in_private_window = exists(PrivateWindow.private_window_pattern,
                                                   FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmark_opened_in_private_window is True, 'The window in which the bookmark is opened is Private'

        page_loaded = exists(LocalWeb.POCKET_IMAGE, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert page_loaded is True, 'The selected website is correctly opened in a new private window.'

        close_window()
