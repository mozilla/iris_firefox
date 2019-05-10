# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Bug 1357098 - Pinned tabs are not restored after browser restart.'
        self.test_case_id = '114816'
        self.test_suite_id = '68'
        self.locales = ['en-US']

    def run(self):
        focus_tab_pattern = Pattern('focus_tab.png')
        focus_pinned_tab_pattern = Pattern('focus_pinned_tab.png')
        firefox_tab_pattern = Pattern('firefox_tab.png')
        firefox_pinned_tab_pattern = Pattern('firefox_pinned_tab.png')
        pin_tab_item_pattern = Pattern('pin_tab_item.png')
        hamburger_menu_button_pattern = NavBar.HAMBURGER_MENU.similar(0.95)
        iris_tab_logo_pattern = Pattern('iris_tab.png')
        if not Settings.is_mac():
            hamburger_menu_quit_item_pattern = Pattern('hamburger_menu_exit.png')

        click_duration = 2

        iris_tab_logo = exists(iris_tab_logo_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, iris_tab_logo, 'Iris tab available')
        iris_tab_logo_location = find(iris_tab_logo_pattern)
        proper_hamburger_menu_region = Region(0, iris_tab_logo_location.y, width=SCREEN_WIDTH, height=SCREEN_HEIGHT/4)

        navigate(LocalWeb.FOCUS_TEST_SITE)

        focus_site_opened = exists(LocalWeb.FOCUS_LOGO, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, focus_site_opened, 'Focus website is properly opened.')

        focus_tab_exists = exists(focus_tab_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, focus_tab_exists, 'Focus tab is available.')

        right_click(focus_tab_pattern)

        pin_tab_item = exists(pin_tab_item_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, pin_tab_item, 'Pin tab item option available')

        click(pin_tab_item_pattern, click_duration)

        focus_tab_pinned = exists(focus_pinned_tab_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, focus_tab_pinned, 'Focus tab successfully pinned.')

        new_window()

        navigate(LocalWeb.FIREFOX_TEST_SITE)

        firefox_test_site_opened = exists(LocalWeb.FIREFOX_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, firefox_test_site_opened, 'Firefox website is properly opened.')

        firefox_test_tab_exists = exists(firefox_tab_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, firefox_test_tab_exists, 'Firefox tab is available.')

        right_click(firefox_tab_pattern)

        pin_tab_item = exists(pin_tab_item_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, pin_tab_item, 'Pin tab item option available')

        click(pin_tab_item_pattern, click_duration)

        firefox_test_tab_pinned = exists(firefox_pinned_tab_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, firefox_test_tab_pinned, 'Firefox tab successfully pinned.')

        # Quit via Hamburger menu
        hamburger_menu_button_exists = exists(hamburger_menu_button_pattern, DEFAULT_FIREFOX_TIMEOUT,
                                              in_region=proper_hamburger_menu_region)
        assert_true(self, hamburger_menu_button_exists, 'Hamburger menu appears on screen.')

        if not Settings.is_mac():
            click(hamburger_menu_button_pattern, DEFAULT_UI_DELAY, in_region=proper_hamburger_menu_region)
            hamburger_menu_quit_displayed = exists(hamburger_menu_quit_item_pattern, DEFAULT_FIREFOX_TIMEOUT)
            assert_true(self, hamburger_menu_quit_displayed, 'Close Firefox from the "Hamburger" menu.')
            click(hamburger_menu_quit_item_pattern, DEFAULT_UI_DELAY)
        else:
            type('q', KeyModifier.CMD)

        #  firefox_runner = None to prevent automatic restore of previous session
        status = self.firefox_runner.process_handler.wait(Settings.FIREFOX_TIMEOUT)
        if status is None:
            self.firefox_runner.stop()
            self.firefox_runner = None

        # keyboard shortcut of method restart_firefox() can break test
        self.firefox_runner = launch_firefox(self.browser.path, self.profile_path, self.base_local_web_url)
        self.firefox_runner.start()

        close_tab()

        firefox_test_tab_pinned = exists(firefox_pinned_tab_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, firefox_test_tab_pinned, 'Firefox tab is pinned after restart.')

        close_window()

        focus_tab_pinned = exists(focus_pinned_tab_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, focus_tab_pinned, 'Focus tab is pinned after restart.')

        assert_true(self, firefox_test_tab_pinned and focus_tab_pinned,
                    'Browser starts with two windows. Both "example.com" and "example.org" are pinned and available in '
                    'respective windows.\n\n Note: old builds affected by this bug have shown this behavior: "Browser '
                    'started with two windows. Only "example.com" pinned tab has been restored in its window. Second '
                    'window contains two blank tabs. "example.org" pinned tab has been lost."')
