# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'Copy a website from the History sidebar and paste it into the URL bar.'

    def setup(self):
        """Test case setup

        This overrides the setup method in the BaseTest class, so that it can use a brand new profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.BRAND_NEW
        return

    def run(self):
        search_history_box = 'search_history_box.png'
        expand_button_history_sidebar = 'expand_button_history_sidebar.png'

        # Open a page to create some history.
        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, expected_1, 'Mozilla page loaded successfully.')
        close_tab()

        # Open the History sidebar.
        history_sidebar()
        expected_2 = exists(search_history_box, 10)
        assert_true(self, expected_2, 'Sidebar was opened successfully.')
        expected_3 = exists(expand_button_history_sidebar, 10)
        assert_true(self, expected_3, 'Expand history button displayed properly.')
        click(expand_button_history_sidebar)

        # Copy a website from the History sidebar and paste it into the URL bar.
        expected_4 = exists(LocalWeb.MOZILLA_BOOKMARK_SMALL, 10)
        assert_true(self, expected_4, 'Mozilla page is displayed in the History list successfully.')

        right_click(LocalWeb.MOZILLA_BOOKMARK_SMALL)
        type(text='c')
        select_location_bar()
        edit_paste()
        type(Key.ENTER)

        # Check that the page was opened successfully.
        expected_5 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, expected_5, 'Mozilla page loaded successfully.')
