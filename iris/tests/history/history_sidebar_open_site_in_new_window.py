# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This is a test that opens a page from the History sidebar using the \'Open in a New Window\' ' \
                    'button from the context menu.'
        self.test_case_id = '120121'
        self.test_suite_id = '2000'
        self.locales = ['en-US']

    def run(self):
        history_sidebar_mozilla = LocalWeb.MOZILLA_BOOKMARK_SMALL
        search_history_box_pattern = Sidebar.HistorySidebar.SEARCH_BOX
        sidebar_history_today_pattern = Sidebar.HistorySidebar.Timeline.TODAY

        left_upper_corner = Region(0, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        # Open some pages to create some history.
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, expected_1, 'Mozilla page loaded successfully.')

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)
        expected_2 = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected_2, 'Firefox page loaded successfully.')

        # Open the History sidebar.
        history_sidebar()
        expected_3 = exists(search_history_box_pattern, 10)
        assert_true(self, expected_3, 'Sidebar was opened successfully.')

        expected_4 = exists(sidebar_history_today_pattern, 10)
        assert_true(self, expected_4, 'Expand history button displayed properly.')
        click(sidebar_history_today_pattern)

        # Open a page from the History sidebar using the 'Open in a New Window' button from the context menu.

        expected_5 = left_upper_corner.exists(history_sidebar_mozilla.similar(0.7), 10)
        assert_true(self, expected_5, 'Mozilla page is displayed in the History list successfully.')

        right_click(history_sidebar_mozilla.similar(0.7), 1)
        time.sleep(Settings.FX_DELAY)
        type(text='n')

        expected_6 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, expected_6, 'Mozilla page loaded successfully.')
