# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='Open all bookmarks from the Bookmarks Toolbar',
        locale=['en-US'],
        test_case_id='165207',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self):
        getting_started_toolbar_bookmark_pattern = Pattern('getting_started_in_toolbar.png')
        mozilla_support_logo_pattern = Pattern('mozilla_support_logo.png')
        open_all_in_tabs_option_pattern = Pattern('open_all_in_tabs.png')

        open_bookmarks_toolbar()

        toolbar_opened = exists(getting_started_toolbar_bookmark_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert toolbar_opened, 'The Bookmarks Toolbar is successfully enabled.'

        getting_started_bookmark_location = find(getting_started_toolbar_bookmark_pattern)
        click_location_x_offset = Screen.SCREEN_WIDTH // 2
        click_location_y_offset = getting_started_toolbar_bookmark_pattern.get_size()[1] // 2

        getting_started_bookmark_location.offset(click_location_x_offset, click_location_y_offset)

        right_click(getting_started_bookmark_location)

        open_all_in_tabs_option_available = exists(open_all_in_tabs_option_pattern)
        assert open_all_in_tabs_option_available, \
            'Context menu is opened, \'Open all in tabs\' option available'

        click(open_all_in_tabs_option_pattern)

        getting_started_page_opened = exists(mozilla_support_logo_pattern, Settings.SITE_LOAD_TIMEOUT)
        getting_started_opened_in_separate_tab = exists(LocalWeb.IRIS_LOGO_INACTIVE_TAB)
        assert getting_started_page_opened and getting_started_opened_in_separate_tab, \
            'All the websites bookmarked are opened in tabs properly'
