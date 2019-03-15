# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This is a test case that restarts the browser.'
        self.enabled = False

    def setup(self):
        """ Test case setup
        This overrides the setup method in the BaseTest class,
        so that it can use a profile that already has been launched.
        """
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        region = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)

        navigate(LocalWeb.FIREFOX_TEST_SITE)
        expected = region.exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Firefox page loaded successfully.')

        restart_firefox(self,
                        self.browser.path,
                        self.profile_path,
                        LocalWeb.MOZILLA_TEST_SITE,
                        image=LocalWeb.MOZILLA_LOGO)

        expected = region.exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, expected, 'Mozilla page loaded successfully.')

        return
