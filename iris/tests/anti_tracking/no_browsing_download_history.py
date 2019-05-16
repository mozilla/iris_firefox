# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Firefox can be set to no longer remember browsing and download history.'
        self.test_case_id = '105208'
        self.test_suite_id = '1826'
        self.locale = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.set_profile_pref({'browser.download.dir': IrisCore.get_downloads_dir()})
        self.set_profile_pref({'browser.download.folderList': 2})
        self.set_profile_pref({'browser.download.useDownloadDir': True})
        downloads_cleanup()

    def teardown(self):
        downloads_cleanup()

    def run(self):
        remember_history_pattern = Pattern('remember_history.png')
        remember_browsing_download_pattern = Pattern('remember_browsing_history.png')
        unticked_browsing_download_pattern = Pattern('remember_browsing_unticked.png')
        custom_history_settings_pattern = Pattern('custom_history_settings.png')
        download_pdf_pattern = Pattern('download_pdf_button.png')
        pdf_downloaded = Pattern('downloaded_pdf.png')

        new_tab()
        navigate('about:preferences#privacy')
        preferences_opened = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED)
        assert_true(self, preferences_opened,
                    'The "about:preferences#privacy" page is successfully displayed')

        paste('remember')
        remember_history_menu_found = exists(remember_history_pattern)
        assert_true(self, remember_history_menu_found, 'History menu found')

        click(remember_history_pattern)
        click(custom_history_settings_pattern)
        use_custom_settings_selected = exists(custom_history_settings_pattern)
        assert_true(self, use_custom_settings_selected,
                    'The "Use custom settings for history" option is successfully selected.')

        click(remember_browsing_download_pattern)
        point_unpinned = exists(unticked_browsing_download_pattern)
        assert_true(self, point_unpinned,
                    'The "Remember my browsing and download history" checkbox is successfully unticked.')
        close_tab()

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)
        firefox_test_site_opened = exists(LocalWeb.FIREFOX_LOGO, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, firefox_test_site_opened, 'Firefox test site opened.')
        close_tab()

        new_tab()
        navigate(LocalWeb.FOCUS_TEST_SITE)
        focus_test_site_opened = exists(LocalWeb.FOCUS_LOGO, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, focus_test_site_opened, 'Focus test site opened.')
        close_tab()

        new_tab()
        navigate(LocalWeb.POCKET_TEST_SITE)
        pocket_site_opened = exists(LocalWeb.POCKET_LOGO, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, pocket_site_opened, 'Pocket site opened')
        close_tab()

        click(NavBar.LIBRARY_MENU)
        library_dropdown_opened = exists(LibraryMenu.HISTORY_BUTTON)
        assert_true(self, library_dropdown_opened, 'Library dropdown opened.')

        click(LibraryMenu.HISTORY_BUTTON)
        firefox_test_site_not_in_history = not exists(LocalWeb.FIREFOX_BOOKMARK_SMALL)
        assert_true(self, firefox_test_site_not_in_history, 'First site not in history.')

        focus_test_site_not_in_history = not exists(LocalWeb.FOCUS_BOOKMARK_SMALL)
        assert_true(self, focus_test_site_not_in_history, 'Second site not in history.')

        pocket_site_not_in_history = not exists(LocalWeb.POCKET_BOOKMARK_SMALL)
        assert_true(self, pocket_site_not_in_history,
                    'Third site not in history.')

        restore_firefox_focus()

        new_tab()
        navigate('https://www.stmarys-ca.edu/sites/default/files/attachments/files/Faust.pdf')
        pdf_bar_located = exists(download_pdf_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, pdf_bar_located, 'PDF loaded')

        click(download_pdf_pattern)
        save_file_dialog_exists = exists(DownloadDialog.SAVE_FILE_RADIOBUTTON, DEFAULT_FIREFOX_TIMEOUT*3)
        assert_true(self, save_file_dialog_exists, 'Save file dialog opened')

        click(DownloadDialog.SAVE_FILE_RADIOBUTTON)
        ok_button_exists = exists(DownloadDialog.OK_BUTTON, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, ok_button_exists, 'Button OK exists')

        click(DownloadDialog.OK_BUTTON)

        download_finished = exists(NavBar.DOWNLOADS_BUTTON)
        assert_true(self, download_finished, 'The pdf document is successfully downloaded.')

        restart_firefox(self, self.browser.path, self.profile_path, self.base_local_web_url)

        open_downloads()
        file_not_in_downloads = not exists(pdf_downloaded)
        assert_true(self, file_not_in_downloads,
                    'The previously downloaded pdf file is not displayed in Firefox download history.')
        click_window_control('close')
