# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = "Firefox can be set to never remember browsing history."
        self.test_case_id = "102381"
        self.test_suite_id = "1956"
        self.locale = ["en-US"]

    def run(self):
        remember_history_pattern = Pattern("remember_history.png")
        never_remember_pattern = Pattern("never_remember_history.png")
        restart_firefox_pattern = Pattern("restart_firefox_button.png")

        new_tab()
        navigate("about:preferences#privacy")
        preferences_opened = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED)
        assert_true(self, preferences_opened, "Preferences tab opened")

        paste("remember")
        remember_history_menu_found = exists(remember_history_pattern)
        assert_true(self, remember_history_menu_found, "History menu found")

        click(remember_history_pattern)
        never_remember_item_found = exists(never_remember_pattern)
        assert_true(self, never_remember_item_found, "Drop-down opened")

        click(never_remember_pattern)
        popup_window_opened = exists(restart_firefox_pattern)
        assert_true(self, popup_window_opened, "Restart popup opened")

        click(restart_firefox_pattern)
        firefox_restarted = exists(Tabs.NEW_TAB_HIGHLIGHTED, DEFAULT_FIREFOX_TIMEOUT * 2)
        assert_true(self, firefox_restarted, "Browser restarted")
        restore_firefox_focus()

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)
        firefox_test_site_opened = exists(LocalWeb.FIREFOX_LOGO, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, firefox_test_site_opened, "Firefox test site opened")
        close_tab()

        new_tab()
        navigate(LocalWeb.FOCUS_TEST_SITE)
        focus_test_site_opened = exists(LocalWeb.FOCUS_LOGO, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, focus_test_site_opened, "Focus test site opened")
        close_tab()

        new_tab()
        navigate(LocalWeb.POCKET_TEST_SITE)
        pocket_site_opened = exists(LocalWeb.POCKET_LOGO, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, pocket_site_opened, "Pocket site opened")
        close_tab()

        click(NavBar.LIBRARY_MENU)
        library_dropdown_opened = exists(LibraryMenu.HISTORY_BUTTON)
        assert_true(self, library_dropdown_opened, "Library dropdown opened")

        click(LibraryMenu.HISTORY_BUTTON)
        firefox_test_site_not_in_history = not exists(LocalWeb.FIREFOX_BOOKMARK_SMALL)
        focus_test_site_not_in_history = not exists(LocalWeb.FOCUS_BOOKMARK_SMALL)
        pocket_site_not_in_history = not exists(LocalWeb.POCKET_BOOKMARK_SMALL)

        assert_true(self, firefox_test_site_not_in_history and
                    focus_test_site_not_in_history and pocket_site_not_in_history, "Visited sites are not in history")
