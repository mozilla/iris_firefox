# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Open a website in a private window and then check it is not displayed in the Recent History list.'
        self.test_case_id = '118806'
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
        recent_history_default_pattern = Pattern('recent_history_default.png')

        # Open a website in a new private window.
        new_private_window()

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        test_site_loaded = exists(LocalWeb.MOZILLA_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, test_site_loaded, 'Mozilla page loaded successfully.')

        # Check that the previously opened page is not displayed in the Recent History list.
        library_button_exists = exists(NavBar.LIBRARY_MENU)
        assert_true(self, library_button_exists, 'Library button exists')

        click(NavBar.LIBRARY_MENU)

        history_button_exists = exists(LibraryMenu.HISTORY_BUTTON, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, history_button_exists, 'History button exists')

        click(LibraryMenu.HISTORY_BUTTON)

        page_not_displayed = exists(recent_history_default_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, page_not_displayed, 'Mozilla page is not displayed in the History list.')
