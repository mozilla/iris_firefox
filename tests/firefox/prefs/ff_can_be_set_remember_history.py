# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Firefox can be successfully set to Remember history',
        locale=['en-US'],
        test_case_id='143603',
        test_suite_id='2241',
    )
    def run(self, firefox):
        remember_history_selected_pattern = Pattern('remember_history_selected.png')

        select_location_bar()
        edit_copy()
        start_url = get_clipboard()
        restore_firefox_focus()

        navigate('about:preferences#privacy')

        preferences_opened = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED)
        assert preferences_opened, 'Preferences page is successfully displayed on privacy block'

        paste('firefox will')
        remember_history_menu_found = exists(remember_history_selected_pattern)
        assert remember_history_menu_found, 'History menu found, Firefox already set to remember history'

        navigate(LocalWeb.FIREFOX_TEST_SITE)
        firefox_site_loaded = exists(LocalWeb.FIREFOX_LOGO, Settings.site_load_timeout)
        assert firefox_site_loaded, 'Firefox local web page is loaded'

        navigate(LocalWeb.FOCUS_TEST_SITE)
        focus_site_loaded = exists(LocalWeb.FOCUS_IMAGE, Settings.site_load_timeout)
        assert focus_site_loaded, 'Focus local web page is loaded'

        navigate(LocalWeb.POCKET_TEST_SITE)
        iris_page_loaded = exists(LocalWeb.POCKET_IMAGE, Settings.site_load_timeout)
        assert iris_page_loaded, 'Iris local page is loaded'

        navigate(start_url)
        start_page_loaded = exists(LocalWeb.IRIS_LOGO)
        assert start_page_loaded, 'Start iris page is loaded'

        library_menu_button_reachable = exists(NavBar.LIBRARY_MENU)
        assert library_menu_button_reachable, 'Library menu button is reachable'

        click(NavBar.LIBRARY_MENU)

        history_block_reachable = exists(LibraryMenu.HISTORY_BUTTON)
        assert history_block_reachable, 'History block is reachable'

        click(LibraryMenu.HISTORY_BUTTON)

        firefox_page_visited = exists(LocalWeb.FIREFOX_BOOKMARK)
        assert firefox_page_visited, 'Firefox local page visit was saved in history'

        focus_page_visited = exists(LocalWeb.FOCUS_BOOKMARK)
        assert focus_page_visited, 'Focus local page visit was saved in history'

        pocket_page_visited = exists(LocalWeb.POCKET_BOOKMARK)
        assert pocket_page_visited, 'Pocket local page visit was saved in history'

        restore_firefox_focus()
