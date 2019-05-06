# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Open all bookmarks from the Bookmarks Toolbar'
        self.test_case_id = '165207'
        self.test_suite_id = '2525'
        self.locale = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        getting_started_toolbar_bookmark_pattern = Pattern('getting_started_in_toolbar.png')
        mozilla_support_logo_pattern = Pattern('mozilla_support_logo.png')
        open_all_in_tabs_option_pattern = Pattern('open_all_in_tabs.png')

        open_bookmarks_toolbar()

        toolbar_opened = exists(getting_started_toolbar_bookmark_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, toolbar_opened, 'The Bookmarks Toolbar is successfully enabled.')

        getting_started_bookmark_location = find(getting_started_toolbar_bookmark_pattern)
        click_location_x_offset = SCREEN_WIDTH // 2
        click_location_y_offset = getting_started_toolbar_bookmark_pattern.get_size()[1] // 2

        getting_started_bookmark_location.offset(click_location_x_offset, click_location_y_offset)

        right_click(getting_started_bookmark_location)

        open_all_in_tabs_option_available = exists(open_all_in_tabs_option_pattern)
        assert_true(self, open_all_in_tabs_option_available,
                    'Context menu is opened, \'Open all in tabs\' option available')

        click(open_all_in_tabs_option_pattern)

        getting_started_page_opened = exists(mozilla_support_logo_pattern, Settings.SITE_LOAD_TIMEOUT)
        getting_started_opened_in_separate_tab = exists(LocalWeb.IRIS_LOGO_INACTIVE_TAB)
        assert_true(self, getting_started_page_opened and getting_started_opened_in_separate_tab,
                    'All the websites bookmarked are opened in tabs properly')
