# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'Delete a time range from the History sidebar.'
        self.test_case_id = '120134'
        self.test_suite_id = '2000'
        self.locales = ['en-US']

    def setup(self):
        """Test case setup

        This overrides the setup method in the BaseTest class, so that it can use a brand new profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.BRAND_NEW
        self.set_profile_pref("browser.warnOnQuit;false")

        return

    def run(self):
        search_history_box_pattern = Pattern('search_history_box.png')
        expand_button_history_sidebar_pattern = Pattern('expand_button_history_sidebar.png')

        # Open a page to create some history.
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, expected_1, 'Mozilla page loaded successfully.')

        # Open the History sidebar.
        history_sidebar()
        expected_2 = exists(search_history_box_pattern, 10)
        assert_true(self, expected_2, 'Sidebar was opened successfully.')
        expected_3 = exists(expand_button_history_sidebar_pattern, 10)
        assert_true(self, expected_3, 'Expand history button displayed properly.')

        # Delete a time range from the History sidebar.
        right_click(expand_button_history_sidebar_pattern)
        type(text='d')
        expected_4 = exists(expand_button_history_sidebar_pattern, 5)
        assert_false(self, expected_4, 'Time range was deleted successfully from the history sidebar.')
