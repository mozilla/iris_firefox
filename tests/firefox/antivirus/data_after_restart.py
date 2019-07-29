# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='No data loss after forced restart.',
        locale=['en-US'],
        test_case_id='217874',
        test_suite_id='3063'
    )
    def run(self, firefox):
        browser_console_pattern = Pattern('browser_console_opened.png')
        wikipedia_logo_pattern = Pattern('wiki_logo.png')
        youtube_logo_pattern = Pattern('youtube_logo.png')
        cnn_logo_unactive_tab_pattern = Pattern('cnn_logo_unactive_tab.png')
        youtube_logo_unactive_tab_pattern = Pattern('youtube_logo_unactive_tab.png').similar(.6)
        wiki_logo_unactive_tab_pattern = Pattern('wiki_logo_unactive_tab.png')

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_opened = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert soap_wiki_opened, 'SOAP Wiki site successfully opened'

        new_tab()

        navigate('https://edition.cnn.com')

        close_content_blocking_pop_up()

        cnn_page_opened = exists(LocalWeb.CNN_LOGO, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT)
        assert cnn_page_opened, 'The CNN site successfully opened'

        history_sidebar()

        history_sidebar_opened = exists(Sidebar.HistorySidebar.SIDEBAR_HISTORY_TITLE, FirefoxSettings.FIREFOX_TIMEOUT)
        assert history_sidebar_opened, 'History sidebar opened'

        history_sidebar_location = find(Sidebar.HistorySidebar.SIDEBAR_HISTORY_TITLE)
        history_width, history_height = Sidebar.HistorySidebar.SIDEBAR_HISTORY_TITLE.get_size()
        history_sidebar_region = Region(0, history_sidebar_location.y, history_width * 3, Screen.SCREEN_HEIGHT / 2)

        today_timeline_exists = exists(Sidebar.HistorySidebar.Timeline.TODAY)
        assert today_timeline_exists, 'The Today timeline displayed'

        click(Sidebar.HistorySidebar.Timeline.TODAY)

        history_updated_cnn = exists(LocalWeb.CNN_LOGO.similar(.6), FirefoxSettings.FIREFOX_TIMEOUT,
                                     region=history_sidebar_region)
        assert history_updated_cnn, 'The CNN site is added to history'

        history_updated_wiki = exists(wikipedia_logo_pattern, region=history_sidebar_region)
        assert history_updated_wiki, 'The Wikipedia site is added to history'

        home_width, home_height = NavBar.HOME_BUTTON.get_size()
        bookmarks_toolbar_location = find(NavBar.HOME_BUTTON)
        bookmarks_toolbar_region = Region(0, bookmarks_toolbar_location.y, Screen.SCREEN_WIDTH, home_height * 4)
        tabs_region = Region(0, 0, Screen.SCREEN_WIDTH, home_height * 4)

        bookmark_page()

        type('CNN')

        folder_option_button_exists = exists(Bookmarks.StarDialog.PANEL_FOLDER_DEFAULT_OPTION.similar(.6))
        assert folder_option_button_exists, 'Folder option button exists'

        click(Bookmarks.StarDialog.PANEL_FOLDER_DEFAULT_OPTION.similar(.6))

        toolbar_option_button_exists = exists(Bookmarks.StarDialog.PANEL_OPTION_BOOKMARK_TOOLBAR.similar(.6))
        assert toolbar_option_button_exists, 'Toolbar option button exists'

        click(Bookmarks.StarDialog.PANEL_OPTION_BOOKMARK_TOOLBAR.similar(.6))

        panel_option_button_exists = exists(Bookmarks.StarDialog.DONE)
        assert panel_option_button_exists, 'Panel option button exists'

        click(Bookmarks.StarDialog.DONE)

        previous_tab()

        bookmark_page()

        type('Wiki')

        folder_option_button_exists = exists(Bookmarks.StarDialog.PANEL_FOLDER_DEFAULT_OPTION.similar(.6))
        assert folder_option_button_exists, 'Folder option button exists'

        click(Bookmarks.StarDialog.PANEL_FOLDER_DEFAULT_OPTION.similar(.6))

        toolbar_option_button_exists = exists(Bookmarks.StarDialog.PANEL_OPTION_BOOKMARK_TOOLBAR.similar(.6))
        assert toolbar_option_button_exists, 'Toolbar option button exists'

        click(Bookmarks.StarDialog.PANEL_OPTION_BOOKMARK_TOOLBAR.similar(.6))

        panel_option_button_exists = exists(Bookmarks.StarDialog.DONE)
        assert panel_option_button_exists, 'Panel option button exists'

        click(Bookmarks.StarDialog.DONE)

        cnn_bookmark_added = exists(LocalWeb.CNN_LOGO, FirefoxSettings.FIREFOX_TIMEOUT, bookmarks_toolbar_region)
        assert cnn_bookmark_added, 'The CNN bookmark is successfully added'

        wiki_bookmark_added = exists(LocalWeb.CNN_LOGO, FirefoxSettings.FIREFOX_TIMEOUT, bookmarks_toolbar_region)
        assert wiki_bookmark_added, 'The Wikipedia bookmark is successfully added'

        new_tab()

        navigate('https://www.youtube.com/')

        youtube_opened = exists(youtube_logo_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert youtube_opened, 'The Youtube site successfully opened'

        new_tab()

        navigate(LocalWeb.POCKET_TEST_SITE)

        pocket_opened = exists(LocalWeb.POCKET_IMAGE, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert pocket_opened, 'The Pocket site successfully opened'

        for _ in range(3):
            open_browser_console()
            browser_console_opened = exists(browser_console_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            if browser_console_opened:
                break

        assert browser_console_opened, 'Browser console displayed'

        restart_via_console()

        browser_console_reopened = exists(browser_console_pattern, FirefoxSettings.FIREFOX_TIMEOUT)

        if browser_console_reopened:
            assert browser_console_reopened, 'Browser console reopened'

            click(browser_console_pattern)

            close_window_control('auxiliary')

        firefox_is_restarted = exists(NavBar.HOME_BUTTON, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT)
        assert firefox_is_restarted, 'Firefox is successfully restarted'

        restore_firefox_focus()

        cnn_bookmark_restored = exists(LocalWeb.CNN_LOGO, FirefoxSettings.FIREFOX_TIMEOUT, bookmarks_toolbar_region)
        assert cnn_bookmark_restored, 'The CNN bookmark is successfully restored'

        wiki_bookmark_restored = exists(LocalWeb.CNN_LOGO, region=bookmarks_toolbar_region)
        assert wiki_bookmark_restored, 'The Wikipedia bookmark is successfully restored'

        history_restored_cnn = exists(LocalWeb.CNN_LOGO.similar(.6), region=history_sidebar_region)
        assert history_restored_cnn, 'The CNN site is added to history'

        history_restored_wiki = exists(wikipedia_logo_pattern, region=history_sidebar_region)
        assert history_restored_wiki, 'The Wikipedia site is added to history'

        history_restored_youtube = exists(youtube_logo_pattern, region=history_sidebar_region)
        assert history_restored_youtube, 'The Youtube site is added to history'

        history_restored_pocket = exists(LocalWeb.POCKET_BOOKMARK_SMALL, region=history_sidebar_region)
        assert history_restored_pocket, 'The Pocket site is added to history'

        tab_restored_cnn = exists(cnn_logo_unactive_tab_pattern.similar(.6), region=tabs_region)
        assert tab_restored_cnn, 'The CNN tab is restored'

        tab_restored_wiki = exists(wiki_logo_unactive_tab_pattern, region=tabs_region)
        assert tab_restored_wiki, 'The Wikipedia tab is restored'

        tab_restored_youtube = exists(youtube_logo_unactive_tab_pattern, region=tabs_region)
        assert tab_restored_youtube, 'The Youtube tab is restored'

        tab_restored_pocket = exists(LocalWeb.POCKET_BOOKMARK_SMALL, region=tabs_region)
        assert tab_restored_pocket, 'The Pocket tab is restored'
