# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="History is correctly remembered after reopening a Normal window and a Private window from the "
        "dock with the same profile ",
        test_case_id="120454",
        test_suite_id="1826",
        locale=["en-US"],
        exclude=[OSPlatform.WINDOWS, OSPlatform.LINUX],
    )
    def run(self, firefox):
        wiki_soap_history_icon_pattern = Pattern("wiki_soap_history_icon.png")
        mozilla_history_item_pattern = LocalWeb.MOZILLA_BOOKMARK_HISTORY_SIDEBAR
        mozilla_history_item_gray_pattern = Pattern(
            "mozilla_bookmark_history_sidebar_grey.png"
        )

        dock_region = Region(
            0 + Screen.SCREEN_WIDTH // 2,
            int(0.8 * Screen.SCREEN_HEIGHT),
            Screen.SCREEN_WIDTH // 2,
            int(0.2 * Screen.SCREEN_HEIGHT),
        )

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        new_private_window()
        private_browsing_window_opened = exists(
            PrivateWindow.private_window_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
        )
        assert (
            private_browsing_window_opened is True
        ), "Private Browsing window is successfully opened."

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_label_exists = exists(
            LocalWeb.SOAP_WIKI_SOAP_LABEL, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT
        )
        assert soap_label_exists is True, "The page is successfully loaded."

        close_window()

        all_windows_closed = exists(Tabs.NEW_TAB_HIGHLIGHTED, 1)
        assert all_windows_closed is False, "The windows are closed"

        firefox_dock_icon_size_1_pattern = Pattern("firefox_dock_icon_size_1.png")
        firefox_dock_icon_size_2_pattern = Pattern("firefox_dock_icon_size_2.png")
        firefox_dock_icon_size_3_pattern = Pattern("firefox_dock_icon_size_3.png")
        firefox_dock_icon_size_4_pattern = Pattern("firefox_dock_icon_size_4.png")
        firefox_dock_icon_size_5_pattern = Pattern("firefox_dock_icon_size_5.png")
        firefox_dock_icon_size_6_pattern = Pattern("firefox_dock_icon_size_6.png")
        firefox_dock_icon_size_7_pattern = Pattern("firefox_dock_icon_size_7.png")
        firefox_dock_icon_size_8_pattern = Pattern("firefox_dock_icon_size_8.png")
        firefox_dock_icon_size_9_pattern = Pattern("firefox_dock_icon_size_9.png")
        firefox_dock_icon_size_10_pattern = Pattern("firefox_dock_icon_size_10.png")
        firefox_dock_icon_size_11_pattern = Pattern("firefox_dock_icon_size_11.png")
        firefox_dock_icon_size_12_pattern = Pattern("firefox_dock_icon_size_12.png")
        firefox_dock_icon_size_13_pattern = Pattern("firefox_dock_icon_size_13.png")
        firefox_dock_icon_size_14_pattern = Pattern("firefox_dock_icon_size_14.png")

        dock_icon_patterns = [
            firefox_dock_icon_size_1_pattern,
            firefox_dock_icon_size_2_pattern,
            firefox_dock_icon_size_3_pattern,
            firefox_dock_icon_size_4_pattern,
            firefox_dock_icon_size_5_pattern,
            firefox_dock_icon_size_6_pattern,
            firefox_dock_icon_size_7_pattern,
            firefox_dock_icon_size_8_pattern,
            firefox_dock_icon_size_9_pattern,
            firefox_dock_icon_size_10_pattern,
            firefox_dock_icon_size_11_pattern,
            firefox_dock_icon_size_12_pattern,
            firefox_dock_icon_size_13_pattern,
            firefox_dock_icon_size_14_pattern,
        ]

        firefox_icon_dock_exists = False
        firefox_icon_dock_location = None

        for dock_icon_pattern in dock_icon_patterns:

            firefox_icon_dock_exists = dock_region.exists(
                dock_icon_pattern.similar(0.81), timeout=1
            )

            if firefox_icon_dock_exists is True:
                firefox_icon_dock_location = find(dock_icon_pattern.similar(0.81))
                break

        assert (
            firefox_icon_dock_exists is True
        ), "The Firefox icon is still visible in the dock."

        right_click(firefox_icon_dock_location)

        new_window_item_exists = exists(
            Docker.NEW_WINDOW_MENU_ITEM, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
        )
        assert new_window_item_exists is True, "New window menu item exists."

        click(Docker.NEW_WINDOW_MENU_ITEM, 1)

        new_window_opened = exists(
            Tabs.NEW_TAB_HIGHLIGHTED, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
        )
        assert (
            new_window_opened is True
        ), "The Normal Browsing window is successfully opened."

        history_sidebar()

        type("Mozilla")

        mozilla_history_item_exists = exists(
            mozilla_history_item_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
        )
        mozilla_history_item_gray = exists(
            mozilla_history_item_gray_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
        )
        assert (
            mozilla_history_item_exists or mozilla_history_item_gray
        ), "Websites visited previously in the Normal window are displayed in the History section"

        for dock_icon_pattern in dock_icon_patterns:

            firefox_icon_dock_exists = dock_region.exists(
                dock_icon_pattern.similar(0.81), timeout=1
            )

            if firefox_icon_dock_exists is True:
                firefox_icon_dock_location = find(dock_icon_pattern)
                break

        assert (
            firefox_icon_dock_exists is True
        ), "The Firefox icon is still visible in the dock."

        right_click(firefox_icon_dock_location)

        new_private_window_item_exists = exists(
            Docker.NEW_PRIVATE_WINDOW_MENU_ITEM, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
        )
        assert (
            new_private_window_item_exists is True
        ), "New private window menu item exists."

        click(Docker.NEW_PRIVATE_WINDOW_MENU_ITEM, 1)

        private_browsing_window_opened = exists(
            PrivateWindow.private_window_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
        )
        assert (
            private_browsing_window_opened is True
        ), "Private Browsing window is successfully opened."

        history_sidebar()

        type("soap")

        wiki_soap_history_icon_exists = exists(wiki_soap_history_icon_pattern, 2)
        assert (
            wiki_soap_history_icon_exists is False
        ), "The website is not displayed in the Recent History section."

        edit_select_all()
        edit_delete()

        type("Mozilla")

        mozilla_history_item_exists = exists(
            mozilla_history_item_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
        )
        mozilla_history_item_gray = exists(
            mozilla_history_item_gray_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
        )

        assert (
            mozilla_history_item_exists or mozilla_history_item_gray
        ), "Websites visited previously in the Normal window are displayed in the History section"
