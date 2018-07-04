# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'Open a website from the Recent History list in a private window.'

    def setup(self):
        """Test case setup

        This overrides the setup method in the BaseTest class, so that it can use a brand new profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.BRAND_NEW
        return

    def run(self):
        recent_history_mozilla = LocalWeb.MOZILLA_BOOKMARK

        # Open a page to create some history.
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, expected_1, 'Mozilla page loaded successfully.')

        # Click on a page from the History list in a private window.
        new_private_window()
        open_library_menu('History')
        screen = get_screen()
        right_upper_corner = Region(screen.getW() / 2, screen.getY(), screen.getW() / 2, screen.getH() / 2)
        expected_2 = right_upper_corner.exists(recent_history_mozilla, 10)
        assert_true(self, expected_2, 'Mozilla page displayed in the History list successfully.')
        right_upper_corner.click(recent_history_mozilla)

        # Check that the page was opened successfully.
        expected_3 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, expected_3, 'Mozilla page loaded successfully.')
