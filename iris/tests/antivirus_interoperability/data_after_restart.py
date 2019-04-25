# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = "No data loss after forced restart"
        self.test_case_id = "217874"
        self.test_suite_id = "3063"
        self.locale = ["en-US"]

    def run(self):
        browser_console_pattern = Pattern('browser_console_opened.png')
        wikipedia_logo_pattern = Pattern('wiki_logo.png')
        youtube_logo_pattern = Pattern('youtube_logo.png')
        twitter_logo_pattern = Pattern('twitter_favicon.png').similar(.75)
        cnn_logo_unactive_tab_pattern = Pattern('cnn_logo_unactive_tab.png')
        youtube_logo_unactive_tab_pattern = Pattern('youtube_logo_unactive_tab.png')
        wiki_logo_unactive_tab_pattern = Pattern('wiki_logo_unactive_tab.png')

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_opened = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, soap_wiki_opened, 'SOAP Wiki site successfully opened')

        new_tab()

        navigate('https://edition.cnn.com')

        cnn_page_opened = exists(LocalWeb.CNN_LOGO, Settings.HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, cnn_page_opened, 'The CNN site successfully opened')

        history_sidebar()

        history_sidebar_opened = exists(Sidebar.HistorySidebar.SIDEBAR_HISTORY_TITLE, Settings.FIREFOX_TIMEOUT)
        assert_true(self, history_sidebar_opened, 'History sidebar opened')

        history_sidebar_location = find(Sidebar.HistorySidebar.SIDEBAR_HISTORY_TITLE)
        history_width, history_height = Sidebar.HistorySidebar.SIDEBAR_HISTORY_TITLE.get_size()
        history_sidebar_region = Region(0, history_sidebar_location.y, history_width * 3, SCREEN_HEIGHT / 2)

        today_timeline_exists = exists(Sidebar.HistorySidebar.Timeline.TODAY)
        assert_true(self, today_timeline_exists, 'The Today timeline displayed')

        click(Sidebar.HistorySidebar.Timeline.TODAY)

        history_updated_cnn = exists(LocalWeb.CNN_LOGO.similar(.6), Settings.FIREFOX_TIMEOUT,
                                     in_region=history_sidebar_region)
        assert_true(self, history_updated_cnn, 'The CNN site is added to history')

        history_updated_wiki = exists(wikipedia_logo_pattern, in_region=history_sidebar_region)
        assert_true(self, history_updated_wiki, 'The Wikipedia site is added to history')

        home_width, home_height = NavBar.HOME_BUTTON.get_size()
        bookmarks_toolbar_location = find(NavBar.HOME_BUTTON)
        bookmarks_toolbar_region = Region(0, bookmarks_toolbar_location.y, SCREEN_WIDTH, home_height * 4)
        tabs_region = Region(0, 0, SCREEN_WIDTH, home_height * 4)

        bookmark_page()

        click(Bookmarks.StarDialog.PANEL_FOLDER_DEFAULT_OPTION.similar(.6), 0)

        click(Bookmarks.StarDialog.PANEL_OPTION_BOOKMARK_TOOLBAR.similar(.6))

        click(Bookmarks.StarDialog.DONE)

        previous_tab()

        bookmark_page()

        click(Bookmarks.StarDialog.PANEL_FOLDER_DEFAULT_OPTION.similar(.6), 0)

        click(Bookmarks.StarDialog.PANEL_OPTION_BOOKMARK_TOOLBAR.similar(.6))

        click(Bookmarks.StarDialog.DONE)

        cnn_bookmark_added = exists(LocalWeb.CNN_LOGO, Settings.FIREFOX_TIMEOUT, bookmarks_toolbar_region)
        assert_true(self, cnn_bookmark_added, 'The CNN bookmark is successfully added')

        wiki_bookmark_added = exists(LocalWeb.CNN_LOGO, Settings.FIREFOX_TIMEOUT, bookmarks_toolbar_region)
        assert_true(self, wiki_bookmark_added, 'The Wikipedia bookmark is successfully added')

        new_tab()

        navigate('https://www.youtube.com/')

        youtube_opened = exists(youtube_logo_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, youtube_opened, 'The Youtube site successfully opened')

        new_tab()

        navigate('https://twitter.com/')

        twitter_opened = exists(twitter_logo_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, twitter_opened, 'The Twitter site successfully opened')

        for _ in range(3):
            open_browser_console()
            browser_console_opened = exists(browser_console_pattern, Settings.FIREFOX_TIMEOUT)
            if browser_console_opened:
                break

        assert_true(self, browser_console_opened, 'Browser console displayed')

        restart_via_console()

        browser_console_reopened = exists(browser_console_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, browser_console_reopened, 'Browser console reopened')

        click(browser_console_pattern)

        close_window_control('auxiliary')

        firefox_is_restarted = exists(NavBar.HOME_BUTTON, Settings.HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, firefox_is_restarted, 'Firefox is successfully restarted')

        restore_firefox_focus()

        cnn_bookmark_restored = exists(LocalWeb.CNN_LOGO, Settings.FIREFOX_TIMEOUT, bookmarks_toolbar_region)
        assert_true(self, cnn_bookmark_restored, 'The CNN bookmark is successfully restored')

        wiki_bookmark_restored = exists(LocalWeb.CNN_LOGO, in_region=bookmarks_toolbar_region)
        assert_true(self, wiki_bookmark_restored, 'The Wikipedia bookmark is successfully restored')

        history_restored_cnn = exists(LocalWeb.CNN_LOGO.similar(.6), in_region=history_sidebar_region)
        assert_true(self, history_restored_cnn, 'The CNN site is added to history')

        history_restored_wiki = exists(wikipedia_logo_pattern, in_region=history_sidebar_region)
        assert_true(self, history_restored_wiki, 'The Wikipedia site is added to history')

        history_restored_youtube = exists(youtube_logo_pattern, in_region=history_sidebar_region)
        assert_true(self, history_restored_youtube, 'The Youtube site is added to history')

        history_restored_twitter = exists(twitter_logo_pattern, in_region=history_sidebar_region)
        assert_true(self, history_restored_twitter, 'The Twitter site is added to history')

        tab_restored_cnn = exists(cnn_logo_unactive_tab_pattern.similar(.6), in_region=tabs_region)
        assert_true(self, tab_restored_cnn, 'The CNN tab is restored')

        tab_restored_wiki = exists(wiki_logo_unactive_tab_pattern, in_region=tabs_region)
        assert_true(self, tab_restored_wiki, 'The Wikipedia tab is restored')

        tab_restored_youtube = exists(youtube_logo_unactive_tab_pattern, in_region=tabs_region)
        assert_true(self, tab_restored_youtube, 'The Youtube tab is restored')

        tab_restored_twitter = exists(twitter_logo_pattern, in_region=tabs_region)
        assert_true(self, tab_restored_twitter, 'The Twitter tab is restored')
