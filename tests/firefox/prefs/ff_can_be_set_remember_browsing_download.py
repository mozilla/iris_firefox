# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *
from targets.firefox.firefox_ui.helpers.download_manager_utils import downloads_cleanup


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Firefox can be set to remember browsing and downloaded history',
        test_case_id='143608',
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
        custom_history_settings_pattern = Pattern('custom_history_settings.png')
        remember_search_history_pattern = Pattern('remember_search_form_history.png')
        prefs_checked_box_pattern = Pattern('prefs_checked_box.png')
        prefs_unchecked_box_pattern = Pattern('prefs_unchecked_box.png')
        download_pdf_pattern = Pattern('download_pdf_button.png')
        pdf_downloaded = Pattern('downloaded_pdf.png')

        pdf_file = self.get_asset_path('Faust.pdf')
        ui_timeout = 1

        box_width, box_heigth = prefs_checked_box_pattern.get_size()

        navigate('about:preferences#privacy')
        preferences_opened = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED)
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

        click(prefs_checked_box_pattern, region=remember_search_history_region)

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

        navigate(pdf_file)

        hamburger_menu_reachable = exists(NavBar.HAMBURGER_MENU)
        assert hamburger_menu_reachable, 'Hamburger menu button is reachable'

        click(NavBar.HAMBURGER_MENU)

        restore_firefox_focus()

        pdf_may_be_downloaded = exists(download_pdf_pattern, Settings.site_load_timeout)
        assert pdf_may_be_downloaded, 'PDF file may be downloaded'

        click(download_pdf_pattern)

        save_file_dialog_exists = exists(DownloadDialog.SAVE_FILE_RADIOBUTTON)
        assert save_file_dialog_exists, 'Save file dialog opened'

        click(DownloadDialog.SAVE_FILE_RADIOBUTTON)

        ok_button_exists = exists(DownloadDialog.OK_BUTTON)
        assert ok_button_exists, 'Button OK exists'

        click(DownloadDialog.OK_BUTTON)

        download_finished = exists(NavBar.DOWNLOADS_BUTTON_BLUE)
        assert download_finished, 'Download is finished'

        new_tab()

        navigate(LocalWeb.FIREFOX_TEST_SITE)
        firefox_page_loaded = exists(LocalWeb.FIREFOX_LOGO, Settings.site_load_timeout)
        assert firefox_page_loaded, 'Firefox local page is loaded'

        navigate(LocalWeb.FOCUS_TEST_SITE)
        focus_page_loaded = exists(LocalWeb.FOCUS_LOGO, Settings.site_load_timeout)
        assert focus_page_loaded, 'Focus local page is loaded'

        navigate(LocalWeb.POCKET_TEST_SITE)
        pocket_page_loaded = exists(LocalWeb.POCKET_IMAGE, Settings.site_load_timeout)
        assert pocket_page_loaded, 'Focus local page is loaded'

        navigate(LocalWeb.BLANK_PAGE)

        navigation_bar_reachable = exists(NavBar.LIBRARY_MENU)
        assert navigation_bar_reachable, 'Navigation bar reachable'

        click(NavBar.LIBRARY_MENU)

        sidebar_menu_bar_opened = exists(Sidebar.HistorySidebar.SIDEBAR_HISTORY_ICON)
        assert sidebar_menu_bar_opened, 'Sidebar is opened'

        click(Sidebar.HistorySidebar.SIDEBAR_HISTORY_ICON)

        history_submenu_opened = exists(History.HistoryMenu.VIEW_HISTORY_SIDEBAR)
        assert history_submenu_opened, 'History submenu is opened'

        firefox_page_not_visited = exists(LocalWeb.FIREFOX_BOOKMARK, ui_timeout)
        assert firefox_page_not_visited, 'Firefox local page visit was saved in history'

        focus_page_not_visited = exists(LocalWeb.FOCUS_BOOKMARK, ui_timeout)
        assert focus_page_not_visited, 'Focus local page visit was saved in history'

        pocket_page_not_visited = exists(LocalWeb.POCKET_BOOKMARK.similar(0.9), ui_timeout)
        assert pocket_page_not_visited, 'Pocket local page visit was saved in history'

        restore_firefox_focus()

        open_library()
        library_opened = exists(Library.DOWNLOADS)
        assert library_opened, 'Library is opened'

        click(Library.DOWNLOADS)

        file_in_downloads = exists(pdf_downloaded)
        assert file_in_downloads, 'The previously downloaded pdf file is displayed in Firefox download history.'

        click_window_control('close')

    def teardown(self):
        downloads_cleanup()

        if exists(Library.TITLE, 0.5):
            click_window_control('close')

        if exists(NavBar.HOME_BUTTON, 0.5):
            restore_firefox_focus()
            quit_firefox()
