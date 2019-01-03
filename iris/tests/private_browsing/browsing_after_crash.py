# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Private Browsing window is not restored after Firefox crash'
        self.test_case_id = '101748'
        self.test_suite_id = '1826'
        self.locales = ['en-US']

    def run(self):
        restart_firefox_button_pattern = Pattern('restart_firefox_button.png')
        soap_wikipedia_header_label_pattern = Pattern('soap_wikipedia_header_label.png')

        restart_firefox(self,
                        self.browser.path,
                        self.profile_path,
                        LocalWeb.FIREFOX_TEST_SITE,
                        image=LocalWeb.FIREFOX_LOGO,
                        show_crash_reporter=True)

        new_private_window()
        private_browsing_window_opened = exists(PrivateWindow.private_window_pattern, 5)
        assert_true(self, private_browsing_window_opened, 'Private Browsing Window opened')

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)
        soap_label_exists = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, 20)
        assert_true(self, soap_label_exists, 'The page is successfully loaded.')

        navigate('about:crashparent')

        if Settings.is_windows():
            crash_reporter_icon_pattern = Pattern('crash_reporter_icon.png')
            crash_reporter_icon_exists = exists(crash_reporter_icon_pattern, 180)
            assert_true(self, crash_reporter_icon_exists, 'Crash Reporter icon exists')
            click(crash_reporter_icon_pattern)

        firefox_crashed = exists(restart_firefox_button_pattern, 10)
        assert_true(self, firefox_crashed, 'Firefox crashed.')

        click(restart_firefox_button_pattern)

        try:
            crash_report_dismissed = wait_vanish(restart_firefox_button_pattern, 180)
            assert_true(self, crash_report_dismissed, 'Crash report dismissed')
        except FindError:
            raise FindError('Crash report is not dismissed')

        restore_session_exists = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, restore_session_exists, 'Firefox restored')

        wiki_label_exists = exists(soap_wikipedia_header_label_pattern, 2)
        assert_false(self, wiki_label_exists, 'The Private Browsing window is not restored.')
