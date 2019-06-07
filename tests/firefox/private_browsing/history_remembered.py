# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='History is correctly remembered after reopening a Normal window and a Private window from the ' 
                    'dock with the same profile ',
        test_case_id='120454',
        test_suite_id='1826',
        locale=['en-US'],
        exclude=[OSPlatform.WINDOWS, OSPlatform.LINUX]
    )
    def run(self, firefox):
        wiki_soap_history_icon_pattern = Pattern('wiki_soap_history_icon.png')
        mozilla_history_item_pattern = Pattern('mozilla_history_item.png')

        dock_region = Region(0, 0.8 * Screen.SCREEN_HEIGHT, Screen.SCREEN_WIDTH, Screen.SCREEN_HEIGHT)

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        new_private_window()
        private_browsing_window_opened = exists(PrivateWindow.private_window_pattern,
                                                FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert private_browsing_window_opened is True, 'Private Browsing window is successfully opened.'

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)
        soap_label_exists = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert soap_label_exists is True, 'The page is successfully loaded.'

        close_window()
        close_window()

        all_windows_closed = exists(Tabs.NEW_TAB_HIGHLIGHTED, 1)
        assert all_windows_closed is False, 'The windows are closed'

        firefox_icon_dock_exists = exists(Docker.FIREFOX_DOCKER_ICON, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert firefox_icon_dock_exists is True, 'The Firefox icon is still visible in the dock.'

        right_click(Docker.FIREFOX_DOCKER_ICON, region=dock_region)

        new_window_item_exists = exists(Docker.NEW_WINDOW_MENU_ITEM, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert new_window_item_exists is True, 'New window menu item exists.'

        click(Docker.NEW_WINDOW_MENU_ITEM)

        new_window_opened = exists(Tabs.NEW_TAB_HIGHLIGHTED, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert new_window_opened is True, 'The Normal Browsing window is successfully opened.'

        history_sidebar()

        type('Mozilla')

        mozilla_history_item_exists = exists(mozilla_history_item_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert mozilla_history_item_exists is True, 'Websites visited previously in the Normal ' \
                                                    'window are displayed in the History section'

        right_click(Docker.FIREFOX_DOCKER_ICON, region=dock_region)

        new_private_window_item_exists = exists(Docker.NEW_PRIVATE_WINDOW_MENU_ITEM,
                                                FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert new_private_window_item_exists is True, 'New private window menu item exists.'

        click(Docker.NEW_PRIVATE_WINDOW_MENU_ITEM)
        private_browsing_window_opened = exists(PrivateWindow.private_window_pattern,
                                                FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert private_browsing_window_opened is True, 'Private Browsing window is successfully opened.'

        history_sidebar()

        type('soap')
        wiki_soap_history_icon_exists = exists(wiki_soap_history_icon_pattern, 2)
        assert wiki_soap_history_icon_exists is False, 'The website is not displayed in the Recent History section.'

        edit_select_all()
        edit_delete()

        type('Mozilla')
        mozilla_history_item_exists = exists(mozilla_history_item_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert mozilla_history_item_exists is True, 'Websites visited previously in the Normal ' \
                                                    'window are displayed in the History section'
