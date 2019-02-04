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
        browser_console_pattern = Pattern('browser_console_opened.png')
        folder_other_bookmarks = Pattern('editBMPanel_folderMenuList_default_Other_Bookmarks.png')
        folder_toolbar_menu = Pattern('editBMPanel_chooseFolderMenuItem_Bookmarks_Toolbar.png')

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_opened = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, soap_wiki_opened, 'SOAP Wiki site successfully opened')

        new_tab()

        navigate('https://edition.cnn.com')

        cnn_page_opened = exists(cnn_page_downloaded_pattern, DEFAULT_HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, cnn_page_opened, 'The CNN site successfully opened')

        close_content_blocking_pop_up()

        history_sidebar()
        click(Library.HISTORY_TODAY)

        history_updated = exists(history_updated_pattern)
        assert_true(self, history_updated, 'History updated')

        location_for_click = find(NavBar.HOME_BUTTON).right(100)

        right_click(location_for_click)
        time.sleep(DEFAULT_UI_DELAY)
        click(toolbar_bookmarks_toolbar_pattern)

        if Settings.is_linux():
            bookmark_page()
            click(folder_other_bookmarks)
            click(folder_toolbar_menu)
            type(Key.ENTER)
        
            previous_tab()
        
            bookmark_page()
            click(folder_other_bookmarks)
            click(folder_toolbar_menu)
            type(Key.ENTER)
        else:
            bookmark_page()
            click(SidebarBookmarks.OTHER_BOOKMARKS)
            click(SidebarBookmarks.BOOKMARKS_TOOLBAR_MENU)
            type(Key.ENTER)

            previous_tab()

            bookmark_page()
            click(SidebarBookmarks.OTHER_BOOKMARKS)
            click(SidebarBookmarks.BOOKMARKS_TOOLBAR_MENU)
            type(Key.ENTER)

        bookmarks_added = exists(bookmarks_restored_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, bookmarks_added, 'The bookmarks are successfully added')

        open_browser_console()
        time.sleep(DEFAULT_UI_DELAY_LONG)
        restart_via_console()

        browser_console_opened = exists(browser_console_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, browser_console_opened, 'Browser console displayed')
        click(browser_console_pattern)
        time.sleep(DEFAULT_UI_DELAY)
        close_window_control('auxiliary')

        all_tabs_are_restored = exists(tabs_restored_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, all_tabs_are_restored, 'The tabs are successfully restored')

        all_bookmarks_are_restored = exists(bookmarks_restored_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, all_bookmarks_are_restored, 'The bookmarks are successfully restored')

        history_are_restored = exists(history_updated_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, history_are_restored, 'The history is successfully restored')






