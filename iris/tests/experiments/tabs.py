# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This is a test of a bunch of tabs'
        self.enabled = False

    def run(self):
        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        expected = exists(LocalWeb.MOZILLA_LOGO, 5)
        assert_true(self, expected, 'Mozilla logo image found.')

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE_2)
        expected = exists(LocalWeb.FIREFOX_LOGO, 5)
        assert_true(self, expected, 'Firefox logo image found.')

        new_tab()
        navigate(LocalWeb.POCKET_TEST_SITE)
        expected = exists(LocalWeb.POCKET_LOGO, 5)
        assert_true(self, expected, 'Pocket logo image found.')

        new_tab()
        navigate(LocalWeb.BLANK_PAGE)

        new_tab()
        new_tab()
        new_tab()
        new_tab()

        navigate(LocalWeb.FOCUS_TEST_SITE)
        expected = exists(LocalWeb.FOCUS_LOGO, 5)
        assert_true(self, expected, 'Focus logo image found.')
