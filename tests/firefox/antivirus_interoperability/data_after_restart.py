# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='No data loss after forced restart.',
        locale=[Locales.ENGLISH],
        test_case_id='217874',
        test_suite_id='3063'
    )
    def test_run(self, firefox):
        toolbar_bookmarks_toolbar_pattern = Pattern('toolbar_bookmarks_toolbar.png')
        browser_console_pattern = Pattern('browser_console_opened.png')
        wikipedia_logo_pattern = Pattern('wiki_logo.png')
        youtube_logo_pattern = Pattern('youtube_logo.png')
        twitter_logo_pattern = Pattern('twitter_favicon.png')
        cnn_logo_unactive_tab_pattern = Pattern('cnn_logo_unactive_tab.png')
        wiki_logo_unactive_tab_pattern = Pattern('wiki_logo_unactive_tab.png')

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)
        assert exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, Settings.DEFAULT_SITE_LOAD_TIMEOUT), \
            'SOAP Wiki site successfully opened.'

        new_tab()
        navigate('https://edition.cnn.com')
        assert exists(LocalWeb.CNN_LOGO, Settings.DEFAULT_HEAVY_SITE_LOAD_TIMEOUT), 'The CNN site successfully opened'

        close_content_blocking_pop_up()
        history_sidebar()
        assert exists(Sidebar.HistorySidebar.SIDEBAR_HISTORY_TITLE), 'History sidebar opened.'

        history_sidebar_location = find(Sidebar.HistorySidebar.SIDEBAR_HISTORY_TITLE)
        history_width, history_height = Sidebar.HistorySidebar.SIDEBAR_HISTORY_TITLE.get_size()
        history_sidebar_region = Region(history_sidebar_location.x,
                                        history_sidebar_location.y,
                                        history_width,
                                        Screen.SCREEN_HEIGHT / 2)

        assert exists(Sidebar.HistorySidebar.Timeline.TODAY), 'The Today timeline displayed.'

        click(Sidebar.HistorySidebar.Timeline.TODAY)
        assert history_sidebar_region.exists(LocalWeb.CNN_LOGO.similar(0.6)), 'The CNN site is added to history.'
        assert history_sidebar_region.exists(wikipedia_logo_pattern), 'The Wikipedia site is added to history.'

        right_click(NavBar.HOME_BUTTON.target_offset(100, 0))
        assert exists(toolbar_bookmarks_toolbar_pattern), 'Bookmarks toolbar button displayed.'

        click(toolbar_bookmarks_toolbar_pattern)

        home_width, home_height = NavBar.HOME_BUTTON.get_size()
        bookmarks_toolbar_location = find(NavBar.HOME_BUTTON)
        bookmarks_toolbar_region = Region(0, bookmarks_toolbar_location.y, Screen.SCREEN_WIDTH, home_height * 4)
        tabs_region = Region(0, 0, Screen.SCREEN_WIDTH, home_height * 4)

        bookmark_page()
        click(Bookmarks.StarDialog.PANEL_FOLDER_DEFAULT_OPTION.similar(0.6))
        click(Bookmarks.StarDialog.PANEL_OPTION_BOOKMARK_TOOLBAR.similar(0.6))
        click(Bookmarks.StarDialog.DONE)

        previous_tab()

        bookmark_page()
        click(Bookmarks.StarDialog.PANEL_FOLDER_DEFAULT_OPTION.similar(0.6))
        click(Bookmarks.StarDialog.PANEL_OPTION_BOOKMARK_TOOLBAR.similar(0.6))
        click(Bookmarks.StarDialog.DONE)
        assert bookmarks_toolbar_region.exists(LocalWeb.CNN_LOGO, Settings.DEFAULT_SITE_LOAD_TIMEOUT), \
            'The CNN bookmark is successfully added.'
        assert bookmarks_toolbar_region.exists(LocalWeb.CNN_LOGO, Settings.DEFAULT_SITE_LOAD_TIMEOUT), \
            'The Wikipedia bookmark is successfully added.'

        new_tab()
        navigate('https://www.youtube.com/')
        assert exists(youtube_logo_pattern, Settings.DEFAULT_SITE_LOAD_TIMEOUT), 'The Youtube site successfully opened.'

        new_tab()
        navigate('https://twitter.com/')
        assert exists(twitter_logo_pattern, Settings.DEFAULT_SITE_LOAD_TIMEOUT), 'The Twitter site successfully opened.'

        open_browser_console()
        assert exists(browser_console_pattern, Settings.DEFAULT_SITE_LOAD_TIMEOUT), 'Browser console displayed.'

        restart_via_console()
        assert exists(browser_console_pattern, Settings.DEFAULT_SITE_LOAD_TIMEOUT), 'Browser console reopened.'

        click(browser_console_pattern)
        close_window_control('auxiliary')
        assert exists(NavBar.HOME_BUTTON, 180), 'Firefox is successfully restarted.'

        restore_firefox_focus()
        assert bookmarks_toolbar_region.exists(LocalWeb.CNN_LOGO, Settings.DEFAULT_SITE_LOAD_TIMEOUT), \
            'The CNN bookmark is successfully restored.'
        assert bookmarks_toolbar_region.exists(LocalWeb.CNN_LOGO, Settings.DEFAULT_SITE_LOAD_TIMEOUT), \
            'The Wikipedia bookmark is successfully restored.'
        assert history_sidebar_region.exists(LocalWeb.CNN_LOGO.similar(0.6)), 'The CNN site is added to history.'
        assert history_sidebar_region.exists(wikipedia_logo_pattern), 'The Wikipedia site is added to history.'
        assert history_sidebar_region.exists(youtube_logo_pattern), 'The Youtube site is added to history.'
        assert history_sidebar_region.exists(twitter_logo_pattern), 'The Twitter site is added to history.'
        assert tabs_region.exists(cnn_logo_unactive_tab_pattern.similar(0.6)), 'The CNN tab is restored.'
        assert tabs_region.exists(wiki_logo_unactive_tab_pattern), 'The Wikipedia tab is restored.'
        assert tabs_region.exists(twitter_logo_pattern), 'The Twitter tab is restored.'
