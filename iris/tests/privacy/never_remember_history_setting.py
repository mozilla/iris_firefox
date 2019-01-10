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

        restore_firefox_focus()
        new_tab()
        navigate("about:preferences#privacy")
        remember_history_menu_found = False
        scroll_side = find(NavBar.LIBRARY_MENU)
        scroll_side.offset(0, SCREEN_HEIGHT/10)
        click(scroll_side, 1)
        while not remember_history_menu_found:
            remember_history_menu_found = exists(remember_history_pattern, 1)
            scroll(-500)
        assert_true(self, remember_history_menu_found, "History menu found")

        time.sleep(0.5)
        history_menu = find(remember_history_pattern)
        click(history_menu)
        never_remember_item_found = exists(never_remember_pattern, 3)
        assert_true(self, never_remember_item_found, "Drop-down opened")

        never_remember_item = find(never_remember_pattern)
        click(never_remember_item)
        popup_window_opened = exists(restart_firefox_pattern)
        assert_true(self, popup_window_opened, "Restart popup opened")

        restart_firefox_button = find(restart_firefox_pattern)
        click(restart_firefox_button)

        time.sleep(1)
        restore_firefox_focus()

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)
        firefox_test_site_opened = exists(LocalWeb.FIREFOX_BOOKMARK_SMALL, 10)
        assert_true(self, firefox_test_site_opened, "Firefox test site opened")

        close_tab()
        new_tab()
        navigate(LocalWeb.FOCUS_TEST_SITE)
        focus_test_site_opened = exists(LocalWeb.FOCUS_BOOKMARK_SMALL, 10)
        assert_true(self, focus_test_site_opened, "Focus test site opened")

        close_tab()
        new_tab()
        navigate(LocalWeb.POCKET_TEST_SITE)
        pocket_site_opened = exists(LocalWeb.POCKET_BOOKMARK_SMALL, 10)
        assert_true(self, pocket_site_opened, "Pocket site opened")

        close_tab()
        click(NavBar.LIBRARY_MENU, 1)
        library_dropdown_opened = exists(LibraryMenu.HISTORY_BUTTON)
        assert_true(self, library_dropdown_opened, "Library dropdown opened")

        history_item = find(LibraryMenu.HISTORY_BUTTON)
        history_item_width, history_item_height = LibraryMenu.HISTORY_BUTTON.get_size()
        history_item.offset(history_item_width/2, history_item_height/2)
        click(history_item)

        firefox_test_site_not_in_history = not exists(LocalWeb.FIREFOX_BOOKMARK_SMALL)
        focus_test_site_not_in_history = not exists(LocalWeb.FOCUS_BOOKMARK_SMALL)
        pocket_site_not_in_history = not exists(LocalWeb.POCKET_BOOKMARK_SMALL)

        assert_true(self, firefox_test_site_not_in_history and
                    focus_test_site_not_in_history and pocket_site_not_in_history, "Visited sites not in history")
        time.sleep(60)
