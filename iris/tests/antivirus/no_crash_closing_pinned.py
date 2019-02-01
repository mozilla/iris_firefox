# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = '[Kaspersky] No crash or bluescreen after closing a pinned tab'
        self.test_case_id = '219585'
        self.test_suite_id = '3063'
        self.locale = ['en-US']

    def run(self):
        close_tab_pattern = Pattern('close_tab_item.png')
        pin_tab_pattern = Pattern('pin_tab_item.png')

        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        first_webpage_loaded = exists(LocalWeb.MOZILLA_BOOKMARK, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, first_webpage_loaded, 'First webpage is loaded.')
        right_click(LocalWeb.MOZILLA_BOOKMARK)

        unpinned_dropdown_opened = exists(pin_tab_pattern)
        assert_true(self, unpinned_dropdown_opened, 'Right-click menu for unpinned displayed')
        click(pin_tab_pattern)

        first_tab_pinned = exists(LocalWeb.MOZILLA_BOOKMARK_SMALL)
        assert_true(self, first_tab_pinned, 'First tab pinned')
        right_click(LocalWeb.MOZILLA_BOOKMARK_SMALL)

        pinned_dropdown_opened = exists(close_tab_pattern)
        assert_true(self, pinned_dropdown_opened, 'Right-click menu for pinned displayed')
        click(close_tab_pattern)

        window_displayed = exists(NavBar.HOME_BUTTON)
        assert_true(self, window_displayed, 'Browser window still displays')
