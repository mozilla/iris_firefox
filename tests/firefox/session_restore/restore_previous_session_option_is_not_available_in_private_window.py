# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='\'Restore Previous Session\' option is not available in a private window',
        test_case_id='115426',
        test_suite_id='68',
        locales=Locales.ENGLISH
    )
    def run(self, firefox):
        restore_previous_session_pattern = Pattern('restore_previous_session_item.png')
        hamburger_menu_quit_item_pattern = None
        if not OSHelper.is_mac():
            hamburger_menu_quit_item_pattern = Pattern('hamburger_menu_quit_item.png').similar(0.9)

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)
        firefox_site_opened = exists(LocalWeb.FIREFOX_IMAGE)
        assert firefox_site_opened, 'Firefox webpage is opened'

        new_tab()
        navigate(LocalWeb.FOCUS_TEST_SITE)
        focus_site_opened = exists(LocalWeb.FOCUS_IMAGE)
        assert focus_site_opened, 'Focus webpage is opened'

        if OSHelper.is_mac():
            quit_firefox()
        else:
            hamburger_menu_button_displayed = exists(NavBar.HAMBURGER_MENU)
            assert hamburger_menu_button_displayed, 'Hamburger menu button is displayed'

            click(NavBar.HAMBURGER_MENU)

            quit_firefox_item_exists = exists(hamburger_menu_quit_item_pattern)
            assert quit_firefox_item_exists, '"Quit" item exists'

            click(hamburger_menu_quit_item_pattern)

        firefox.restart()

        new_private_window()
        private_window_opened = exists(PrivateWindow.private_window_pattern)
        assert private_window_opened, 'Private window is opened'

        hamburger_menu_button_displayed = exists(NavBar.HAMBURGER_MENU)
        assert hamburger_menu_button_displayed, 'Hamburger menu button is displayed'

        click(NavBar.HAMBURGER_MENU)

        restore_previous_session_item_still_exists = exists(restore_previous_session_pattern)
        assert restore_previous_session_item_still_exists, '"Restore previous session" item exists'

        click(restore_previous_session_pattern)

        restore_previous_session_item_still_exists = exists(restore_previous_session_pattern)
        assert restore_previous_session_item_still_exists, \
            '\'Restore previous session\' item still exists, session wasn\'t restored'

        restore_firefox_focus()
        close_tab()
