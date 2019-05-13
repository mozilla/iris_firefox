# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Previous Session can be restored from the Firefox menu'
        self.test_case_id = '114837'
        self.test_suite_id = '68'
        self.locales = ['en-US']

    def run(self):
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        test_site_opened = exists(LocalWeb.MOZILLA_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, test_site_opened, 'Mozilla test website is opened')

        new_tab()

        navigate(LocalWeb.POCKET_TEST_SITE)

        test_site_opened = exists(LocalWeb.POCKET_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, test_site_opened, 'Pocket test website is opened')

        if Settings.is_mac():
            quit_firefox()
        elif Settings.is_linux():
            click_hamburger_menu_option('Quit')
        else:
            click_hamburger_menu_option('Exit')

        status = self.firefox_runner.process_handler.wait(Settings.FIREFOX_TIMEOUT)
        if status is None:
            self.firefox_runner.stop()
            self.firefox_runner = None

        self.firefox_runner = launch_firefox(self.browser.path, self.profile_path, self.base_local_web_url)
        self.firefox_runner.start()

        firefox_restarted = exists(LocalWeb.IRIS_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, firefox_restarted, 'Firefox restarted successfully')

        click_hamburger_menu_option('Restore')

        next_tab()

        first_tab_restored = exists(LocalWeb.MOZILLA_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, first_tab_restored, 'Mozilla test website is restored')

        next_tab()

        second_tab_restored = exists(LocalWeb.POCKET_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, second_tab_restored, 'Pocket test website is restored')

        all_tab_restored = first_tab_restored and second_tab_restored
        assert_true(self, all_tab_restored, 'The previous session is successfully restored (All previously closed tabs'
                                            ' are successfully restored).')

