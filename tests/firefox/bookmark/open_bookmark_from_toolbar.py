# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Open a bookmark in a New Tab",
        locale=["en-US"],
        test_case_id="164363",
        test_suite_id="2525",
        blocked_by={"id": "1579898", "platform": OSPlatform.ALL},
        profile=Profiles.TEN_BOOKMARKS,
    )
    def run(self, firefox):
        most_visited_folder_pattern = Pattern("most_visited_bookmarks.png")
        pocket_bookmark_pattern = Pattern("pocket_bookmark_icon.png")
        open_option_pattern = Pattern("open_option.png")

        open_bookmarks_toolbar()

        bookmarks_folder_available_in_toolbar = exists(
            most_visited_folder_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
        )
        assert bookmarks_folder_available_in_toolbar is True, "The 'Bookmarks Toolbar' is enabled."

        click(most_visited_folder_pattern)

        pocket_bookmark_available = exists(pocket_bookmark_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert pocket_bookmark_available is True, (
            "'Pocket' bookmark is available in the 'Most visited' " "folder from the toolbar"
        )

        right_click(pocket_bookmark_pattern)

        open_option_available = exists(open_option_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert open_option_available is True, (
            "'Open' option is available in context menu after right-click " "at the bookmark"
        )

        click(open_option_pattern)

        website_opened_in_current_tab = exists(LocalWeb.POCKET_IMAGE, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert website_opened_in_current_tab is True, "The website is correctly opened in the current tab."

        bookmark_opened_in_current_tab = exists(LocalWeb.IRIS_LOGO_ACTIVE_TAB, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmark_opened_in_current_tab is False, (
            "The page that was previously displayed in the current tab " "is no longer displayed"
        )
