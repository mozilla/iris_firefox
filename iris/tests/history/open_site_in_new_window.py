# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'Open a website in a new window and then check it is displayed in the Recent History list.'

    def setup(self):
        """Test case setup

        This overrides the setup method in the BaseTest class, so that it can use a brand new profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.BRAND_NEW
        return

    def run(self):
        recent_history_mozilla = 'recent_history_mozilla.png'

        # Open a website in a new window.
        new_window()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, expected_1, 'Mozilla page loaded successfully.')

        # Check that the previously opened page is displayed on the top of the Recent History list.
        open_library_menu('History')
        expected_2 = exists(recent_history_mozilla, 10)
        assert_true(self, expected_2, 'Mozilla page displayed in the History list successfully.')
