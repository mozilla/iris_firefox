# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'History is correctly remembered after reopening a Normal window and a Private window from the ' \
                    'dock with the same profile '
        self.test_case_id = '120454'
        self.test_suite_id = '1826'
        self.locales = ['en-US']
        self.exclude = [Platform.WINDOWS, Platform.LINUX]

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.BRAND_NEW
        return

    def run(self):
        soap_label_pattern = Pattern('soap_label.png')
        private_browsing_icon_pattern = Pattern('private_browsing_icon.png')
        new_tab_label_pattern = Pattern('new_tab_label.png')
        firefox_icon_dock_pattern = Pattern('firefox_logo_dock.png')
        new_window_item_pattern = Pattern('new_window_item.png')
        wiki_soap_history_icon_pattern = Pattern('wiki_soap_history_icon.png')
        new_private_window_item_pattern = Pattern('new_private_window_item.png').target_offset(-2, -2)
        mozilla_history_item_pattern = Pattern('mozilla_history_item.png')

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        new_private_window()
        private_browsing_window_opened = exists(private_browsing_icon_pattern, 5)
        assert_true(self, private_browsing_window_opened, 'Private Browsing window is successfully opened.')

        navigate(LocalWeb.WIKI_TEST_SITE)
        soap_label_exists = exists(soap_label_pattern, 20)
        assert_true(self, soap_label_exists, 'The page is successfully loaded.')

        close_window()
        close_window()

        all_windows_closed = exists(new_tab_label_pattern, 1)
        assert_false(self, all_windows_closed, 'The windows are closed')

        firefox_icon_dock_exists = exists(firefox_icon_dock_pattern, 5)
        assert_true(self, firefox_icon_dock_exists, 'The Firefox icon is still visible in the dock.')

        right_click(firefox_icon_dock_pattern)

        new_window_item_exists = exists(new_window_item_pattern, 5)
        assert_true(self, new_window_item_exists, 'New window menu item exists.')

        click(new_window_item_pattern)

        new_window_opened = exists(new_tab_label_pattern, 5)
        assert_true(self, new_window_opened, 'The Normal Browsing window is successfully opened.')

        history_sidebar()

        type('Mozilla')

        mozilla_history_item_exists = exists(mozilla_history_item_pattern, 5)
        assert_true(self, mozilla_history_item_exists, 'Websites visited previously in the Normal window are '
                                                       'displayed in the History section')

        right_click(firefox_icon_dock_pattern)

        new_private_window_item_exists = exists(new_private_window_item_pattern, 5)
        assert_true(self, new_private_window_item_exists, 'New private window menu item exists.')

        click(new_private_window_item_pattern)
        private_browsing_window_opened = exists(private_browsing_icon_pattern, 5)
        assert_true(self, private_browsing_window_opened, 'Private Browsing window is successfully opened.')

        history_sidebar()

        type('soap')
        wiki_soap_history_icon_exists = exists(wiki_soap_history_icon_pattern, 2)
        assert_false(self, wiki_soap_history_icon_exists, 'The website is not displayed in the Recent History section.')

        edit_select_all()
        edit_delete()

        type('Mozilla')
        mozilla_history_item_exists = exists(mozilla_history_item_pattern, 5)
        assert_true(self, mozilla_history_item_exists, 'Websites visited previously in the Normal window are '
                                                       'displayed in the History section')
