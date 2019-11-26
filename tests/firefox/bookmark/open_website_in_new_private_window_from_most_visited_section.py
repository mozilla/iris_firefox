# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Open a website in a new Private Window from 'Most Visited' section using contextual menu",
        locale=["en-US"],
        test_case_id="163201",
        test_suite_id="2525",
        profile=Profiles.TEN_BOOKMARKS,
        exclude=OSPlatform.MAC,
    )
    def run(self, firefox):
        firefox_menu_bookmarks_pattern = Pattern("bookmarks_top_menu.png")
        firefox_menu_bookmarks_toolbar_pattern = Pattern("firefox_menu_bookmarks_toolbar.png")
        firefox_menu_most_visited_pattern = Pattern("firefox_menu_most_visited.png")
        firefox_pocket_bookmark_pattern = Pattern("pocket_most_visited.png")
        open_in_a_new_private_window_pattern = Pattern("context_menu_open_in_a_new_private_window.png")

        open_firefox_menu()

        firefox_menu_bookmarks_exists = exists(firefox_menu_bookmarks_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert firefox_menu_bookmarks_exists is True, "Firefox menu > Bookmarks exists"

        click(firefox_menu_bookmarks_pattern)

        bookmarks_toolbar_folder_exists = exists(
            firefox_menu_bookmarks_toolbar_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
        )
        assert bookmarks_toolbar_folder_exists is True, "Firefox menu > Bookmarks > Bookmarks Toolbar folder exists"

        click(firefox_menu_bookmarks_toolbar_pattern)

        most_visited_folder_exists = exists(firefox_menu_most_visited_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert most_visited_folder_exists is True, (
            "Firefox menu > Bookmarks > Bookmarks Toolbar > Most Visited " "folder exists"
        )

        click(firefox_menu_most_visited_pattern)

        firefox_pocket_bookmark_exists = exists(firefox_pocket_bookmark_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert firefox_pocket_bookmark_exists is True, "Most visited websites are displayed."

        right_click(firefox_pocket_bookmark_pattern, 0)

        open_in_new_private_window_option_exists = exists(
            open_in_a_new_private_window_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
        )
        assert open_in_new_private_window_option_exists is True, "Open in a New Private Window option exists"

        click(open_in_a_new_private_window_pattern)

        firefox_pocket_site_opened = exists(LocalWeb.POCKET_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert firefox_pocket_site_opened is True, "The website is opened"

        site_opened_in_new_private_window = exists(PrivateWindow.private_window_pattern)
        assert site_opened_in_new_private_window is True, (
            "The selected website is correctly opened in a new private" " window."
        )

        close_window()
