# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='No data loss after a forced crash',
        locale=['en-US'],
        test_case_id='219582',
        test_suite_id='3063',
        blocked_by={'id': 'issue_403', 'platform': OSPlatform.ALL}
    )
    def run(self, firefox):
        restart_firefox_button_pattern = Pattern('restart_firefox_button.png')
        wikipedia_logo_pattern = Pattern('wiki_logo.png')
        youtube_logo_pattern = Pattern('youtube_logo.png')
        twitter_logo_pattern = Pattern('twitter_favicon.png')
        cnn_logo_unactive_tab_pattern = Pattern('cnn_logo_unactive_tab.png')
        youtube_logo_unactive_tab_pattern = Pattern('youtube_logo_unactive_tab.png')
        twitter_logo_unactive_tab_pattern = Pattern('twitter_logo_unactive_tab.png')
        wiki_logo_unactive_tab_pattern = Pattern('wiki_logo_unactive_tab.png')
        restore_previous_session_checkbox_pattern = Pattern('restore_previous_session_checkbox.png')

        navigate('about:preferences#general')

        restore_previous_session_checkbox_displayed = exists(restore_previous_session_checkbox_pattern, 10)
        assert restore_previous_session_checkbox_displayed is True, 'Restore previous session button displayed'

        click(restore_previous_session_checkbox_pattern)

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_opened = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert soap_wiki_opened is True, 'SOAP Wiki site successfully opened'

        new_tab()

        navigate('https://edition.cnn.com')

        cnn_page_opened = exists(LocalWeb.CNN_LOGO, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT)
        assert cnn_page_opened, 'The CNN site successfully opened'

        close_content_blocking_pop_up()
        history_sidebar()

        history_sidebar_opened = exists(Sidebar.HistorySidebar.SIDEBAR_HISTORY_TITLE)
        assert history_sidebar_opened is True, 'History sidebar opened'

        history_sidebar_location = find(Sidebar.HistorySidebar.SIDEBAR_HISTORY_TITLE)
        history_width, history_height = Sidebar.HistorySidebar.SIDEBAR_HISTORY_TITLE.get_size()

        history_sidebar_region = Screen().new_region(0, history_sidebar_location.y, history_width * 3,
                                                     Screen.SCREEN_HEIGHT // 2)

        today_timeline_exists = exists(Sidebar.HistorySidebar.Timeline.TODAY, 10)
        assert today_timeline_exists is True, 'The Today timeline displayed'

        click(Sidebar.HistorySidebar.Timeline.TODAY)

        home_width, home_height = NavBar.HOME_BUTTON.get_size()
        bookmarks_toolbar_location = find(NavBar.HOME_BUTTON)

        bookmarks_toolbar_region = Screen().new_region(0, bookmarks_toolbar_location.y, Screen.SCREEN_WIDTH,
                                                       home_height*3)
        tabs_region = Screen().new_region(0, 0, Screen.SCREEN_WIDTH, home_height * 4)

        bookmark_page()

        click(Bookmarks.StarDialog.PANEL_FOLDER_DEFAULT_OPTION.similar(0.6))

        click(Bookmarks.StarDialog.PANEL_OPTION_BOOKMARK_TOOLBAR.similar(0.6))

        click(Bookmarks.StarDialog.DONE)

        previous_tab()

        bookmark_page()

        click(Bookmarks.StarDialog.PANEL_FOLDER_DEFAULT_OPTION.similar(0.6), 0)

        click(Bookmarks.StarDialog.PANEL_OPTION_BOOKMARK_TOOLBAR.similar(0.6))

        click(Bookmarks.StarDialog.DONE)

        cnn_bookmark_added = exists(LocalWeb.CNN_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT, bookmarks_toolbar_region)
        assert cnn_bookmark_added is True, 'The CNN bookmark is successfully added'

        wiki_bookmark_added = exists(LocalWeb.CNN_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT, bookmarks_toolbar_region)
        assert wiki_bookmark_added is True, 'The Wikipedia bookmark is successfully added'

        new_tab()

        navigate('https://www.youtube.com/')

        youtube_opened = exists(youtube_logo_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert youtube_opened is True, 'The Youtube site successfully opened'

        new_tab()

        navigate('https://twitter.com/')

        twitter_opened = exists(twitter_logo_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert twitter_opened is True, 'The Twitter site successfully opened'

        firefox.restart()

        navigate('about:crashparent')

        if OSHelper.is_windows():
            crash_reporter_icon_pattern = Pattern('crash_reporter_icon.png')
            crash_reporter_icon_exists = exists(crash_reporter_icon_pattern, 180)
            assert crash_reporter_icon_exists is True, 'Crash Reporter icon exists'

            click(crash_reporter_icon_pattern)

        firefox_crashed = exists(restart_firefox_button_pattern, 10)
        assert firefox_crashed is True, 'Firefox crashed.'

        click(restart_firefox_button_pattern)

        firefox_is_restarted = exists(NavBar.HOME_BUTTON, 180)
        assert firefox_is_restarted, 'Firefox is successfully restarted'

        restore_firefox_focus()

        cnn_bookmark_restored = exists(LocalWeb.CNN_LOGO, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT,
                                       bookmarks_toolbar_region)
        assert cnn_bookmark_restored is True, 'The CNN bookmark is successfully restored'

        wiki_bookmark_restored = exists(wikipedia_logo_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT,
                                        bookmarks_toolbar_region)
        assert wiki_bookmark_restored is True, 'The Wikipedia bookmark is successfully restored'

        history_restored_cnn = exists(LocalWeb.CNN_LOGO.similar(0.6), region=history_sidebar_region)
        assert history_restored_cnn is True, 'The CNN site is added to history'

        history_restored_wiki = exists(wikipedia_logo_pattern, region=history_sidebar_region)
        assert history_restored_wiki is True, 'The Wikipedia site is added to history'

        history_restored_youtube = exists(youtube_logo_pattern, region=history_sidebar_region)
        assert history_restored_youtube is True, 'The Youtube site is added to history'

        history_restored_twitter = exists(twitter_logo_pattern, region=history_sidebar_region)
        assert history_restored_twitter is True, 'The Twitter site is added to history'

        tab_restored_cnn = exists(cnn_logo_unactive_tab_pattern, region=tabs_region)
        assert tab_restored_cnn is True, 'The CNN tab is restored'

        tab_restored_wiki = exists(wiki_logo_unactive_tab_pattern, region=tabs_region)
        assert tab_restored_wiki is True, 'The Wikipedia tab is restored'

        tab_restored_youtube = exists(youtube_logo_unactive_tab_pattern, region=tabs_region)
        assert tab_restored_youtube is True, 'The Youtube tab is restored'

        tab_restored_twitter = exists(twitter_logo_unactive_tab_pattern, region=tabs_region)
        assert tab_restored_twitter is True, 'The Twitter tab is restored'
