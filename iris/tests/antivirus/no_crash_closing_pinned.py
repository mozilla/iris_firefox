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
        mozilla_tab_pattern = Pattern('mozilla_tab.png')
        mozilla_pinned_tab_pattern = Pattern('mozilla_pinned_tab.png')
        firefox_tab_pattern = Pattern('firefox_tab.png')
        firefox_pinned_tab_pattern = Pattern('firefox_pinned_tab.png')
        focus_tab_pattern = Pattern('focus_tab.png')
        focus_pinned_tab_pattern = Pattern('focus_pinned_tab.png')

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)
        firefox_tab_opened = exists(firefox_tab_pattern)
        assert_true(self, firefox_tab_opened, 'Second webpage is opened')
        right_click(firefox_tab_pattern)
        try:
            click(pin_tab_pattern)
        except FindError:
            raise FindError('No "Pin Tab" item found')

        second_tab_pinned = exists(firefox_pinned_tab_pattern)
        assert_true(self, second_tab_pinned, 'Second tab is pinned')
        new_tab()

        navigate(LocalWeb.FOCUS_TEST_SITE)


        # time.sleep(300)


        focus_tab_opened = exists(focus_tab_pattern)
        assert_true(self, focus_tab_opened, 'Third tab is opened')
        right_click(focus_tab_pattern)
        try:
            click(pin_tab_pattern)
        except FindError:
            raise FindError('No "Pin Tab" item found')

        third_tab_pinned = exists(focus_pinned_tab_pattern)
        assert_true(self, third_tab_pinned, 'Third tab is pinned')

        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        first_webpage_loaded = exists(mozilla_tab_pattern, DEFAULT_SITE_LOAD_TIMEOUT)


        # time.sleep(60)


        assert_true(self, first_webpage_loaded, 'First webpage is loaded.')
        right_click(mozilla_tab_pattern)

        unpinned_dropdown_opened = exists(pin_tab_pattern)


        # time.sleep(60)


        assert_true(self, unpinned_dropdown_opened, 'Right-click menu for unpinned displayed')
        click(pin_tab_pattern)

        first_tab_pinned = exists(mozilla_pinned_tab_pattern)
        assert_true(self, first_tab_pinned, 'First tab is pinned')
        right_click(mozilla_pinned_tab_pattern)
        pinned_dropdown_opened = exists(close_tab_pattern)
        assert_true(self, pinned_dropdown_opened, 'Right-click menu for pinned displayed')
        click(close_tab_pattern)

        try:
            click(NavBar.HAMBURGER_MENU)
            hamburger_menu_opened = exists(HamburgerMenu.ADDONS)
            assert_true(self, hamburger_menu_opened, 'Hamburger menu is opened, Firefox didn\'t crash.')
        except FindError:
            raise FindError('Unable to interact with hamburger menu')
        # time.sleep(60)
