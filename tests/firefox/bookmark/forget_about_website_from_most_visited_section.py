# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Forget About a site from \'Most Visited\' section',
        locale=['en-US'],
        test_case_id='163205',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS,
        exclude=OSPlatform.MAC
    )
    def run(self, firefox):
        firefox_menu_bookmarks_pattern = Pattern('firefox_menu_bookmarks.png')
        firefox_menu_bookmarks_toolbar_pattern = Pattern('firefox_menu_bookmarks_toolbar.png')
        firefox_menu_most_visited_pattern = Pattern('firefox_menu_most_visited.png')
        firefox_pocket_bookmark_pattern = Pattern('pocket_most_visited.png')
        forget_about_this_site_option_pattern = Pattern('forget_about_this_site_option.png')

        history_sidebar()

        history_sidebar_opened = exists(Sidebar.HistorySidebar.SIDEBAR_HISTORY_TITLE)
        assert history_sidebar_opened is True, 'History sidebar opened'

        history_sidebar_location = find(Sidebar.HistorySidebar.SIDEBAR_HISTORY_TITLE)
        history_width, history_height = Sidebar.HistorySidebar.SIDEBAR_HISTORY_TITLE.get_size()
        history_sidebar_region = Region(0, history_sidebar_location.y, history_width * 3, Screen.SCREEN_HEIGHT / 2)

        today_timeline_exists = exists(Sidebar.HistorySidebar.Timeline.TODAY)
        assert today_timeline_exists is True, 'The Today timeline displayed'

        click(Sidebar.HistorySidebar.Timeline.TODAY)

        iris_logo_exists_in_history = exists(LocalWeb.IRIS_LOGO_ACTIVE_TAB, region=history_sidebar_region)
        assert iris_logo_exists_in_history is True, 'Iris logo exists in history'

        open_firefox_menu()

        firefox_menu_bookmarks_exists = exists(firefox_menu_bookmarks_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert firefox_menu_bookmarks_exists is True, 'Firefox menu > Bookmarks exists'

        click(firefox_menu_bookmarks_pattern)

        bookmarks_toolbar_folder_exists = exists(firefox_menu_bookmarks_toolbar_pattern,
                                                 FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmarks_toolbar_folder_exists is True, 'Firefox menu > Bookmarks > Bookmarks Toolbar folder exists'

        click(firefox_menu_bookmarks_toolbar_pattern)

        most_visited_folder_exists = exists(firefox_menu_most_visited_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert most_visited_folder_exists is True, 'Firefox menu > Bookmarks > Bookmarks Toolbar > Most Visited ' \
                                                   'folder exists'

        click(firefox_menu_most_visited_pattern)

        firefox_pocket_bookmark_exists = exists(firefox_pocket_bookmark_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert firefox_pocket_bookmark_exists is True, 'Most visited websites are displayed.'

        right_click(firefox_pocket_bookmark_pattern, 0)

        delete_option_exists = exists(forget_about_this_site_option_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert delete_option_exists is True, 'Forget About This Site option exists'

        click(forget_about_this_site_option_pattern)

        # Here Iris Logo checked for vanishing from history because of all LocalWeb sites have the same URL
        # ((_ip_host, _port) + /something) And when the Pocket site forgotten  all LocalWeb will be forgotten also

        try:
            iris_logo_exists_in_history = wait_vanish(LocalWeb.IRIS_LOGO_ACTIVE_TAB, region=history_sidebar_region)
            assert iris_logo_exists_in_history, 'The website is removed from the history.'
        except FindError:
            raise FindError('The website is not removed from the history.')

        bookmark_forgotten = exists(firefox_pocket_bookmark_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmark_forgotten is False, 'The website is removed from the Most Visited list.'

        restore_firefox_focus()
