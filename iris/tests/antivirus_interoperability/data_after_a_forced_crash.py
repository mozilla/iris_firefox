# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = "No data loss after forced restart"
        self.test_case_id = "217874"
        self.test_suite_id = "3036"
        self.locale = ["en-US"]

    def run(self):
        cnn_page_downloaded_pattern = Pattern('cnn_page_downloaded.png')
        history_updated_pattern = Pattern('history_updated.png')
        toolbar_bookmarks_toolbar_pattern = Pattern('toolbar_bookmarks_toolbar.png')
        tabs_restored_pattern = Pattern('tabs_restored.png')
        bookmarks_restored_pattern = Pattern('bookmarks_restored.png')
        folder_other_bookmarks = Pattern('other_bookmarks.png')
        folder_toolbar_menu = Pattern('editBMPanel_chooseFolderMenuItem_Bookmarks_Toolbar.png')
        history_today_pattern = Pattern('history_today.png')
        restart_firefox_button_pattern = Pattern('restart_firefox_button.png')
        history_region = Region(0, 0, SCREEN_WIDTH / 6, SCREEN_HEIGHT / 3)

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_opened = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, soap_wiki_opened, 'SOAP Wiki site successfully opened')

        new_tab()

        navigate('https://edition.cnn.com')

        cnn_page_opened = exists(cnn_page_downloaded_pattern, DEFAULT_HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, cnn_page_opened, 'The CNN site successfully opened')

        close_content_blocking_pop_up()

        history_sidebar()
        if Settings.is_mac():
            click(history_today_pattern, 0, history_region)
        else:
            click(Library.HISTORY_TODAY, 0, history_region)

        history_updated = exists(history_updated_pattern, None, history_region)
        assert_true(self, history_updated, 'History updated')

        location_for_click = find(NavBar.HOME_BUTTON).right(100)

        right_click(location_for_click)
        time.sleep(DEFAULT_UI_DELAY)
        click(toolbar_bookmarks_toolbar_pattern)

        if Settings.is_linux() or Settings.is_mac():
            bookmark_page()
            click(folder_other_bookmarks, 0)
            click(folder_toolbar_menu, 0)
            time.sleep(DEFAULT_UI_DELAY)
            type(Key.ENTER)
        
            previous_tab()
        
            bookmark_page()
            click(folder_other_bookmarks, 0)
            click(folder_toolbar_menu, 0)
            time.sleep(DEFAULT_UI_DELAY)
            type(Key.ENTER)
        else:
            bookmark_page()
            click(SidebarBookmarks.OTHER_BOOKMARKS, 0)
            click(SidebarBookmarks.BOOKMARKS_TOOLBAR_MENU, 0)
            time.sleep(DEFAULT_UI_DELAY)
            type(Key.ENTER)

            previous_tab()

            bookmark_page()
            click(SidebarBookmarks.OTHER_BOOKMARKS, 0)
            click(SidebarBookmarks.BOOKMARKS_TOOLBAR_MENU, 0)
            time.sleep(DEFAULT_UI_DELAY)
            type(Key.ENTER)

        bookmarks_added = exists(bookmarks_restored_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, bookmarks_added, 'The bookmarks are successfully added')

        restart_firefox(self,
                        self.browser.path,
                        self.profile_path,
                        self.base_local_web_url,
                        show_crash_reporter=True)

        navigate('about:crashparent')

        if Settings.is_windows():
            crash_reporter_icon_pattern = Pattern('crash_reporter_icon.png')
            crash_reporter_icon_exists = exists(crash_reporter_icon_pattern, 180)
            assert_true(self, crash_reporter_icon_exists, 'Crash Reporter icon exists')
            click(crash_reporter_icon_pattern)

        firefox_crashed = exists(restart_firefox_button_pattern, 10)
        assert_true(self, firefox_crashed, 'Firefox crashed.')

        click(restart_firefox_button_pattern)

        try:
            crash_report_dismissed = wait_vanish(restart_firefox_button_pattern, 180)
            assert_true(self, crash_report_dismissed, 'Crash report dismissed')
        except FindError:
            raise FindError('Crash report is not dismissed')

        all_tabs_are_restored = exists(tabs_restored_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, all_tabs_are_restored, 'The tabs are successfully restored')

        all_bookmarks_are_restored = exists(bookmarks_restored_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, all_bookmarks_are_restored, 'The bookmarks are successfully restored')

        history_are_restored = exists(history_updated_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, history_are_restored, 'The history is successfully restored')






