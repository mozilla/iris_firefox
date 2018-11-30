# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'The "Never remember history" settings remain valid after reopening the browser from the dock'
        self.test_case_id = '120453'
        self.test_suite_id = '1826'
        self.locales = ['en-US']

    def setup(self):
        """ Test case setup
        This overrides the setup method in the BaseTest class,
        so that it can use a profile that already has bookmarks.
        """
        BaseTest.setup(self)
        self.profile = Profile.BRAND_NEW
        return

    def run(self):
        browser_privacy_label_pattern = Pattern('browser_privacy_label.png')
        drop_down_toggle_button_pattern = Pattern('drop_down_toggle_button.png')
        never_remember_history_label_pattern = Pattern('never_remember_history_label.png')
        restart_firefox_now_button_pattern = Pattern('restart_firefox_now_button.png')
        firefox_icon_dock_pattern = Pattern('firefox_logo_dock.png')
        new_window_item_pattern = Pattern('new_window_item.png')
        new_private_window_item_pattern = Pattern('new_private_window_item.png').target_offset(-2, -2)
        new_tab_label_pattern = Pattern('new_tab_label.png')
        soap_label_pattern = Pattern('soap_label.png')
        wiki_soap_history_icon_pattern = Pattern('wiki_soap_history_icon.png')

        navigate('about:preferences#privacy')

        privacy_preferences_page_opened = exists(browser_privacy_label_pattern, 10)
        assert_true(self, privacy_preferences_page_opened, 'Privacy page opened.')

        type('never remember')

        drop_down_toggle_button_exists = exists(drop_down_toggle_button_pattern, 5)
        assert_true(self, drop_down_toggle_button_exists, 'Options available')

        click(drop_down_toggle_button_pattern)

        never_remember_history_label_exists = exists(never_remember_history_label_pattern, 5)
        assert_true(self, never_remember_history_label_exists, 'Never remember option available')

        click(never_remember_history_label_pattern)

        restart_firefox_now_button_exists = exists(restart_firefox_now_button_pattern, 5)
        assert_true(self, restart_firefox_now_button_exists, 'The Restart Nightly/Restart Firefox popup is displayed.')

        click(restart_firefox_now_button_pattern)

        private_browsing_icon_exists = exists(new_tab_label_pattern, 10)
        assert_true(self, private_browsing_icon_exists, 'The browser restarted.')

        close_tab()

        right_click(firefox_icon_dock_pattern)
        new_private_window_item_exists = exists(new_private_window_item_pattern, 5)
        assert_true(self, new_private_window_item_exists, 'New Private Window option is available.')
        new_window_item_pattern_not_exists = exists(new_window_item_pattern, 1)
        assert_false(self, new_window_item_pattern_not_exists, 'New Window option is not available.')

        click(new_private_window_item_pattern)
        private_browsing_icon_exists = exists(new_tab_label_pattern, 5)
        assert_true(self, private_browsing_icon_exists, 'The browser opens the new page.')

        navigate(LocalWeb.WIKI_TEST_SITE)
        soap_label_exists = exists(soap_label_pattern, 20)
        assert_true(self, soap_label_exists, 'The page is successfully loaded.')

        history_sidebar()

        type('soap', interval=1)

        wiki_soap_history_icon_exists = exists(wiki_soap_history_icon_pattern, 1)
        assert_false(self, wiki_soap_history_icon_exists, 'The website is not displayed in the Recent History section.')




















