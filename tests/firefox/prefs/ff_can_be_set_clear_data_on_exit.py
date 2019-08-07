# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *
from targets.firefox.firefox_ui.helpers.download_manager_utils import downloads_cleanup


class Test(FirefoxTest):

    @pytest.mark.details(
        description=' Firefox can be customized to clear certain data on exit ',
        test_case_id='143610',
        test_suite_id='2241',
        locale=['en-US'],
        preferences={'browser.download.dir': PathManager.get_downloads_dir(),
                     'browser.download.folderList': 2,
                     'browser.download.useDownloadDir': True}
    )
    def run(self, firefox):
        always_private_pattern = Pattern('always_private.png')
        remember_all_history_pattern = Pattern('remember_history.png')
        remember_browsing_history_pattern = Pattern('remember_browsing_download_history.png')
        clear_history_closing_pattern = Pattern('clear_history_when_closes.png')
        clear_history_settings_pattern = Pattern('clear_history_settings.png')
        custom_history_settings_pattern = Pattern('custom_history_settings.png')
        remember_search_history_pattern = Pattern('remember_search_form_history.png')
        prefs_checked_box_pattern = Pattern('prefs_checked_box.png')
        prefs_unchecked_box_pattern = Pattern('prefs_unchecked_box.png')
        download_pdf_pattern = Pattern('download_pdf_button.png')
        pdf_downloaded_pattern = Pattern('downloaded_pdf.png')
        clear_browsing_download_pattern = Pattern('clear_browsing_download.png').similar(.7)
        clear_form_search_patten = Pattern('clear_form_search.png')

        pdf_file = self.get_asset_path('Faust.pdf')
        ui_timeout = 1
        quick_click_duration = 0.3

        box_width, box_height = prefs_checked_box_pattern.get_size()

        navigate('about:preferences#privacy')
        preferences_opened = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED,
                                    FirefoxSettings.FIREFOX_TIMEOUT)
        assert preferences_opened, 'Preferences page is opened'

        paste('Firefox will')
        history_preferences_reachable = exists(remember_all_history_pattern)
        assert history_preferences_reachable, 'History menu is reachable'

        click(remember_all_history_pattern)

        history_menu_opened = exists(custom_history_settings_pattern)
        assert history_menu_opened, 'History preferences menu is opened'

        click(custom_history_settings_pattern)

        custom_history_settings_opened = exists(always_private_pattern)
        assert custom_history_settings_opened, 'Custom history list is displayed'

        always_private_location = find(always_private_pattern)

        always_private_width, always_private_height = always_private_pattern.get_size()
        always_private_region = Region(always_private_location.x - box_width * 2, always_private_location.y,
                                       always_private_width + box_width * 2, always_private_height)

        always_private_unchecked = exists(prefs_unchecked_box_pattern, region=always_private_region)
        assert always_private_unchecked, '"Always use private browsing mode" is off'

        remember_browsing_displayed = exists(remember_browsing_history_pattern)
        assert remember_browsing_displayed, '"Remember browsing" is displayed'

        remember_browsing_history_location = find(remember_browsing_history_pattern)

        remember_browsing_history_width, remember_browsing_history_height = remember_browsing_history_pattern.get_size()
        remember_browsing_history_region = Region(remember_browsing_history_location.x - box_width * 2,
                                                  remember_browsing_history_location.y,
                                                  remember_browsing_history_width + box_width * 2,
                                                  remember_browsing_history_height)

        remember_browsing_history_checked = exists(prefs_checked_box_pattern, region=remember_browsing_history_region)
        assert remember_browsing_history_checked, '"Always use private browsing mode" is off'

        remember_search_history_displayed = exists(remember_search_history_pattern)
        assert remember_search_history_displayed, '"Remember browsing" is displayed'

        remember_search_history_location = find(remember_search_history_pattern)

        remember_search_history_width, remember_search_history_height = remember_search_history_pattern.get_size()
        remember_search_history_region = Region(remember_search_history_location.x - box_width * 2,
                                                remember_search_history_location.y,
                                                remember_search_history_width + box_width * 2,
                                                remember_search_history_height)

        remember_search_history_checked = exists(prefs_checked_box_pattern, region=remember_search_history_region)
        assert remember_search_history_checked, '"Always use private browsing mode" is off'

        clear_history_closing_displayed = exists(clear_history_closing_pattern)
        assert clear_history_closing_displayed, '"Clear history when closed" is displayed'

        clear_history_closing_location = find(clear_history_closing_pattern)

        clear_history_closing_width, clear_history_closing_height = clear_history_closing_pattern.get_size()
        clear_history_closing_region = Region(clear_history_closing_location.x - box_width * 2,
                                              clear_history_closing_location.y,
                                              clear_history_closing_width + box_width * 2,
                                              clear_history_closing_height)

        clear_history_unchecked = exists(prefs_unchecked_box_pattern, region=clear_history_closing_region)
        assert clear_history_unchecked, '"Clear history" is unchecked'

        click(prefs_unchecked_box_pattern, quick_click_duration, clear_history_closing_region)

        clear_history_settings_button_activated = exists(clear_history_settings_pattern)
        assert clear_history_settings_button_activated, 'History purging settings button is activated'

        click(clear_history_settings_pattern, quick_click_duration)

        clear_history_settings_opened = exists(clear_browsing_download_pattern)
        assert clear_history_settings_opened, '"Clear after exit" settings opened'

        clear_browsing_download_checked = find_in_region_from_pattern(clear_browsing_download_pattern,
                                                                      AboutPreferences.CHECKED_BOX)
        assert clear_browsing_download_checked, '"Clear browsing and download" is checked'

        settings_still_opened = exists(clear_form_search_patten)
        assert settings_still_opened, 'Settings are still opened'

        clear_form_search_checked = find_in_region_from_pattern(clear_form_search_patten, AboutPreferences.CHECKED_BOX)
        assert clear_form_search_checked, '"Clear browsing and download" is checked'

        click(clear_form_search_patten, quick_click_duration)

        clear_form_search_unchecked = find_in_region_from_pattern(clear_form_search_patten,
                                                                  AboutPreferences.UNCHECKED_BOX)
        assert clear_form_search_unchecked, '"Clear form and search" was successfully unchecked'

        type(Key.ENTER)

        settings_closed = exists(clear_history_settings_pattern)
        assert settings_closed, 'History purging menu is closed'

        navigate(LocalWeb.FIREFOX_TEST_SITE)
        firefox_page_loaded = exists(LocalWeb.FIREFOX_LOGO)
        assert firefox_page_loaded, 'Firefox page is loaded'

        navigate(pdf_file)
        pdf_opened = exists(download_pdf_pattern)
        assert pdf_opened, 'Pdf was opened in browser'

        click(download_pdf_pattern)

        save_file_dialog_exists = exists(DownloadDialog.SAVE_FILE_RADIOBUTTON, FirefoxSettings.FIREFOX_TIMEOUT)
        assert save_file_dialog_exists, 'Save file dialog opened'

        click(DownloadDialog.SAVE_FILE_RADIOBUTTON)

        ok_button_exists = exists(DownloadDialog.OK_BUTTON)
        assert ok_button_exists, 'Button OK exists'

        click(DownloadDialog.OK_BUTTON)

        pdf_downloaded = exists(NavBar.DOWNLOADS_BUTTON)
        assert pdf_downloaded, 'Pdf was downloaded'

        navigate(LocalWeb.BLANK_PAGE)

        navbar_displayed = exists(NavBar.LIBRARY_MENU)
        assert navbar_displayed, 'Navigation bar is displayed'

        click(NavBar.LIBRARY_MENU)

        library_menu_opened = exists(LibraryMenu.HISTORY_BUTTON)
        assert library_menu_opened, 'Library menu is opened'

        click(LibraryMenu.HISTORY_BUTTON, quick_click_duration)

        history_menu_opened = exists(History.HistoryMenu.SHOW_ALL_HISTORY)
        assert history_menu_opened, 'History menu is opened'

        move(History.HistoryMenu.SHOW_ALL_HISTORY, quick_click_duration)

        browsing_history_purged = exists(LocalWeb.FIREFOX_BOOKMARK)
        assert browsing_history_purged, 'Browsing history saved so far'

        possible_to_return = exists(Utils.LIBRARY_BACK_BUTTON)
        assert possible_to_return, 'It\'s possible to go back to library menu'

        click(Utils.LIBRARY_BACK_BUTTON, quick_click_duration)

        library_menu_still_opened = exists(LibraryMenu.DOWNLOADS)
        assert library_menu_still_opened, 'Library menu is still opened'

        if OSHelper.is_mac():

            restore_firefox_focus()
            open_library()
            library_window_opened = exists(Library.DOWNLOADS)
            assert library_window_opened, 'Library window is opened'

            click(Library.DOWNLOADS, quick_click_duration)

            download_saved = exists(pdf_downloaded_pattern)
            assert download_saved, 'Downloads are saved so far'

            close_tab()
            library_window_closed = not exists(Library.TITLE, ui_timeout)
            assert library_window_closed, 'Library is closed'

        else:
            click(LibraryMenu.DOWNLOADS, quick_click_duration)

            downloads_menu_opened = exists(DownloadManager.SHOW_ALL_DOWNLOADS)
            assert downloads_menu_opened, 'Downloads menu is opened'

            move(DownloadManager.SHOW_ALL_DOWNLOADS, quick_click_duration)

            download_saved = exists(pdf_downloaded_pattern)
            assert download_saved, 'Downloads are saved so far'

            restore_firefox_focus()

        firefox.restart()

        navbar_displayed = exists(NavBar.LIBRARY_MENU)
        assert navbar_displayed, 'Navigation bar is displayed'

        click(NavBar.LIBRARY_MENU)

        library_menu_opened = exists(LibraryMenu.HISTORY_BUTTON)
        assert library_menu_opened, 'Library menu is opened'

        click(LibraryMenu.HISTORY_BUTTON, quick_click_duration)

        history_menu_opened = exists(History.HistoryMenu.SHOW_ALL_HISTORY)
        assert history_menu_opened, 'History menu is opened'

        move(History.HistoryMenu.SHOW_ALL_HISTORY, quick_click_duration)

        browsing_history_purged = not exists(LocalWeb.FIREFOX_BOOKMARK, ui_timeout)
        assert browsing_history_purged, 'Browsing history was cleared'

        possible_to_return = exists(Utils.LIBRARY_BACK_BUTTON)
        assert possible_to_return, 'It\'s possible to go back to library menu'

        click(Utils.LIBRARY_BACK_BUTTON)

        library_menu_still_opened = exists(LibraryMenu.DOWNLOADS)
        assert library_menu_still_opened, 'Library menu is still opened'

        if OSHelper.is_mac():
            restore_firefox_focus()
            open_library()
            library_window_opened = exists(Library.DOWNLOADS)
            assert library_window_opened, 'Library window is opened'

            click(Library.DOWNLOADS, quick_click_duration)

            download_not_saved = not exists(pdf_downloaded_pattern, ui_timeout)
            assert download_not_saved, 'Downloads are cleared'

            close_tab()

            library_window_closed = not exists(Library.TITLE, ui_timeout)
            assert library_window_closed, 'Library is closed'

        else:
            click(LibraryMenu.DOWNLOADS, quick_click_duration)

            downloads_menu_opened = exists(DownloadManager.SHOW_ALL_DOWNLOADS)
            assert downloads_menu_opened, 'Downloads menu is opened'

            move(DownloadManager.SHOW_ALL_DOWNLOADS, quick_click_duration)

            download_not_saved = not exists(pdf_downloaded_pattern, ui_timeout)
            assert download_not_saved, 'Downloads are cleared'

            restore_firefox_focus()

    @staticmethod
    def teardown():
        downloads_cleanup()
