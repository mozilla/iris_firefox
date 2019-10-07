# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="No data loss after a shutdown (Ffx)",
        locale=["en-US"],
        test_case_id="217880",
        test_suite_id="3063",
    )
    def run(self, firefox):
        restore_previous_session_button_pattern = Pattern(
            "restore_previous_session.png"
        )
        wikipedia_logo_pattern = Pattern("wiki_logo.png")
        firefox_toolbar_bookmark_pattern = Pattern("firefox_toolbar_bookmark.png")

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_opened = exists(
            LocalWeb.SOAP_WIKI_SOAP_LABEL, FirefoxSettings.SITE_LOAD_TIMEOUT
        )
        assert soap_wiki_opened is True, "SOAP Wiki site successfully opened"

        new_tab()

        navigate(LocalWeb.FIREFOX_TEST_SITE)

        firefox_page_opened = exists(
            LocalWeb.FIREFOX_IMAGE, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT
        )
        assert firefox_page_opened is True, "The Firefox site successfully opened"

        history_sidebar()

        history_sidebar_opened = exists(
            Sidebar.HistorySidebar.SIDEBAR_HISTORY_TITLE.similar(0.6)
        )
        assert history_sidebar_opened is True, "History sidebar opened"

        history_sidebar_location = find(Sidebar.HistorySidebar.SIDEBAR_HISTORY_TITLE)
        history_width, history_height = (
            Sidebar.HistorySidebar.SIDEBAR_HISTORY_TITLE.get_size()
        )

        history_sidebar_region = Screen().new_region(
            0, history_sidebar_location.y, history_width * 3, Screen.SCREEN_HEIGHT / 2
        )

        today_timeline_exists = exists(Sidebar.HistorySidebar.Timeline.TODAY)
        assert today_timeline_exists is True, "The Today timeline displayed"

        click(Sidebar.HistorySidebar.Timeline.TODAY)

        history_updated_firefox = exists(
            LocalWeb.FIREFOX_BOOKMARK_SMALL.similar(0.7),
            FirefoxSettings.FIREFOX_TIMEOUT,
            history_sidebar_region,
        )
        assert history_updated_firefox is True, "The Firefox site is added to history"

        history_updated_wiki = exists(
            wikipedia_logo_pattern, region=history_sidebar_region
        )
        assert history_updated_wiki is True, "The Wikipedia site is added to history"

        home_width, home_height = NavBar.HOME_BUTTON.get_size()
        bookmarks_toolbar_location = find(NavBar.HOME_BUTTON)

        bookmarks_toolbar_region = Screen().new_region(
            0, bookmarks_toolbar_location.y, Screen.SCREEN_WIDTH, home_height * 3
        )
        bookmark_page()

        type("Firefox")

        folder_option_button_exists = exists(
            Bookmarks.StarDialog.PANEL_FOLDER_DEFAULT_OPTION.similar(0.6)
        )
        assert folder_option_button_exists, "Folder option button exists"

        click(Bookmarks.StarDialog.PANEL_FOLDER_DEFAULT_OPTION.similar(0.6))

        toolbar_option_button_exists = exists(
            Bookmarks.StarDialog.PANEL_OPTION_BOOKMARK_TOOLBAR.similar(0.6)
        )
        assert toolbar_option_button_exists, "Toolbar option button exists"

        click(Bookmarks.StarDialog.PANEL_OPTION_BOOKMARK_TOOLBAR.similar(0.6))

        panel_option_button_exists = exists(Bookmarks.StarDialog.DONE)
        assert panel_option_button_exists, "Panel option button exists"

        click(Bookmarks.StarDialog.DONE)

        previous_tab()

        bookmark_page()

        type("Wiki")

        folder_option_button_exists = exists(
            Bookmarks.StarDialog.PANEL_FOLDER_DEFAULT_OPTION.similar(0.6)
        )
        assert folder_option_button_exists, "Folder option button exists"

        click(Bookmarks.StarDialog.PANEL_FOLDER_DEFAULT_OPTION.similar(0.6))

        toolbar_option_button_exists = exists(
            Bookmarks.StarDialog.PANEL_OPTION_BOOKMARK_TOOLBAR.similar(0.6)
        )
        assert toolbar_option_button_exists, "Toolbar option button exists"

        click(Bookmarks.StarDialog.PANEL_OPTION_BOOKMARK_TOOLBAR.similar(0.6))

        panel_option_button_exists = exists(Bookmarks.StarDialog.DONE)
        assert panel_option_button_exists, "Panel option button exists"

        click(Bookmarks.StarDialog.DONE)

        firefox_bookmark_added = exists(
            firefox_toolbar_bookmark_pattern,
            FirefoxSettings.SITE_LOAD_TIMEOUT,
            region=bookmarks_toolbar_region,
        )
        assert (
            firefox_bookmark_added is True
        ), "The Firefox bookmark is successfully added"

        wiki_bookmark_added = exists(
            wikipedia_logo_pattern,
            FirefoxSettings.SITE_LOAD_TIMEOUT,
            region=bookmarks_toolbar_region,
        )
        assert (
            wiki_bookmark_added is True
        ), "The Wikipedia bookmark is successfully added"

        new_tab()

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        mozilla_opened = exists(
            LocalWeb.MOZILLA_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT
        )
        assert mozilla_opened is True, "The Mozilla test site successfully opened"

        new_tab()

        navigate(LocalWeb.POCKET_TEST_SITE)

        pocket_opened = exists(LocalWeb.POCKET_IMAGE, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert pocket_opened, "The Pocket site successfully opened"

        firefox.restart(url="", image=NavBar.HOME_BUTTON)

        firefox_is_restarted = exists(
            NavBar.HOME_BUTTON, FirefoxSettings.SITE_LOAD_TIMEOUT
        )
        assert firefox_is_restarted is True, "Firefox is successfully restarted"

        restore_firefox_focus()

        cnn_bookmark_restored = exists(
            firefox_toolbar_bookmark_pattern,
            FirefoxSettings.SITE_LOAD_TIMEOUT,
            bookmarks_toolbar_region,
        )
        assert (
            cnn_bookmark_restored is True
        ), "The Firefox bookmark is successfully restored"

        wiki_bookmark_restored = exists(
            wikipedia_logo_pattern,
            FirefoxSettings.SITE_LOAD_TIMEOUT,
            bookmarks_toolbar_region,
        )
        assert (
            wiki_bookmark_restored is True
        ), "The Wikipedia bookmark is successfully restored"

        click(NavBar.HAMBURGER_MENU)

        restore_previous_session_button_displayed = exists(
            restore_previous_session_button_pattern
        )
        assert (
            restore_previous_session_button_displayed is True
        ), "Restore previous session button displayed"

        click(restore_previous_session_button_pattern)

        history_restored_cnn = exists(
            LocalWeb.FIREFOX_BOOKMARK_SMALL, region=history_sidebar_region
        )
        assert history_restored_cnn is True, "The Firefox site is added to history"

        history_restored_wiki = exists(
            wikipedia_logo_pattern, region=history_sidebar_region
        )
        assert history_restored_wiki is True, "The Wikipedia site is added to history"

        history_restored_mozilla = exists(
            LocalWeb.MOZILLA_BOOKMARK_HISTORY_SIDEBAR, region=history_sidebar_region
        )
        assert history_restored_mozilla is True, "The Mozilla site is added to history"

        history_restored_pocket = exists(
            LocalWeb.POCKET_BOOKMARK_SMALL, region=history_sidebar_region
        )
        assert history_restored_pocket, "The Pocket site is added to history"

        select_tab("1")

        tab_restored_wiki = exists(
            LocalWeb.SOAP_WIKI_SOAP_LABEL, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert tab_restored_wiki is True, "The Wikipedia tab is restored"

        next_tab()

        tab_restored_firefox = exists(
            LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert tab_restored_firefox is True, "The Firefox tab is restored"

        next_tab()

        tab_restored_mozilla = exists(
            LocalWeb.MOZILLA_LOGO, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert tab_restored_mozilla is True, "The Mozilla tab is restored"

        next_tab()

        tab_restored_pocket = exists(
            LocalWeb.POCKET_LOGO, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert tab_restored_pocket, "The Pocket tab is restored"

        cnn_bookmark_still_displayed = exists(
            firefox_toolbar_bookmark_pattern,
            FirefoxSettings.SITE_LOAD_TIMEOUT,
            region=bookmarks_toolbar_region,
        )
        assert (
            cnn_bookmark_still_displayed is True
        ), "The CNN bookmark is still displayed"

        wiki_bookmark_still_displayed = exists(
            wikipedia_logo_pattern,
            FirefoxSettings.SITE_LOAD_TIMEOUT,
            region=bookmarks_toolbar_region,
        )
        assert (
            wiki_bookmark_still_displayed is True
        ), "The Wikipedia bookmark is still displayed"
