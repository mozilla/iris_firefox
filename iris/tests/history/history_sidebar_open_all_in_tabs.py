# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This is a test for the \'Open All in Tabs\' option from the History sidebar.'
        self.test_case_id = '120117'
        self.test_suite_id = '2000'
        self.locales = ['en-US']

    def setup(self):
        """Test case setup

        This overrides the setup method in the BaseTest class, so that it can use a brand new profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.BRAND_NEW

        return

    def run(self):
        firefox_privacy_logo_pattern = Pattern('firefox_privacy_logo.png')
        search_history_box_pattern = Sidebar.HistorySidebar.SEARCH_BOX
        history_today_sidebar_pattern = Sidebar.HistorySidebar.Timeline.TODAY
        iris_logo_pattern = Pattern('iris_logo_tab.png')
        mozilla_logo_pattern = Pattern('mozilla_logo_tab.png')

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
        expected_4 = exists(history_today_sidebar_pattern, 10)
        assert_true(self, expected_4, 'Expand history button displayed properly.')

        # 'Open All in Tabs' from the context menu.
        right_click(history_today_sidebar_pattern)
        time.sleep(Settings.FX_DELAY)
        type(text='o')

        # Check that all the pages loaded successfully.
        expected_5 = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected_5, 'Firefox page loaded successfully.')
        next_tab()
        expected_6 = exists(firefox_privacy_logo_pattern, 10)
        assert_true(self, expected_6, 'Firefox Privacy Notice loaded successfully.')
        expected_7 = exists(iris_logo_pattern, 10)
        assert_true(self, expected_7, 'Iris local page loaded successfully.')
        expected_8 = exists(mozilla_logo_pattern, 10)
        assert_true(self, expected_8, 'Mozilla page loaded successfully.')
