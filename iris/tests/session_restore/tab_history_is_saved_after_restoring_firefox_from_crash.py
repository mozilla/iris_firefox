# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Tab History is saved after restoring Firefox from a crash'
        self.test_case_id = '114828'
        self.test_suite_id = '68'
        self.locales = ['en-US']

    def run(self):
        restart_firefox_button_pattern = Pattern('restart_firefox_button.png')
        restore_previous_session_checkbox_pattern = Pattern('restore_previous_session_checkbox.png')
        if Settings.is_windows():
            crash_reporter_icon_pattern = Pattern('crash_reporter_icon.png')

        navigate('about:preferences#general')

        restore_previous_session_checkbox_displayed = exists(restore_previous_session_checkbox_pattern)
        assert_true(self, restore_previous_session_checkbox_displayed, 'Restore previous session button displayed')

        click(restore_previous_session_checkbox_pattern)

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        test_site_opened = exists(LocalWeb.MOZILLA_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, test_site_opened, 'Mozilla test website is opened')

        navigate(LocalWeb.POCKET_TEST_SITE)

        test_site_opened = exists(LocalWeb.POCKET_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, test_site_opened, 'Pocket test website is opened')

        navigate(LocalWeb.FOCUS_TEST_SITE)

        test_site_opened = exists(LocalWeb.FOCUS_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, test_site_opened, 'Focus test website is opened')

        navigate(LocalWeb.FIREFOX_TEST_SITE)

        test_site_opened = exists(LocalWeb.FIREFOX_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, test_site_opened, 'Firefox test website is opened')

        restart_firefox(self,
                        self.browser.path,
                        self.profile_path,
                        self.base_local_web_url,
                        show_crash_reporter=True)

        navigate('about:crashparent')

        if Settings.is_windows():
            crash_reporter_icon_exists = exists(crash_reporter_icon_pattern, Settings.HEAVY_SITE_LOAD_TIMEOUT)
            assert_true(self, crash_reporter_icon_exists, 'Crash Reporter icon exists')

            click(crash_reporter_icon_pattern)

        firefox_crashed = exists(restart_firefox_button_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, firefox_crashed, 'Firefox crashed.')

        click(restart_firefox_button_pattern)

        firefox_is_restarted = exists(NavBar.HOME_BUTTON, Settings.HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, firefox_is_restarted, 'Firefox is successfully restarted')

        previous_tab()

        test_site_opened = exists(LocalWeb.FIREFOX_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, test_site_opened, 'Firefox test website is restored')

        navigate_back()

        test_site_opened = exists(LocalWeb.FOCUS_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, test_site_opened, 'Focus test website history was successfully remembered.')

        navigate_back()

        test_site_opened = exists(LocalWeb.POCKET_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, test_site_opened, 'Pocket test website history was successfully remembered.')

        navigate_back()

        test_site_opened = exists(LocalWeb.MOZILLA_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, test_site_opened, 'Mozilla test website history was successfully remembered. The tab history '
                                            'was successfully remembered.')
