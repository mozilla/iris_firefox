from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = "Firefox can be set to no longer remember browsing and download history."
        self.test_case_id = "105208"
        self.test_suite_id = "1956"
        self.locale = ["en-US"]

    def run(self):
        remember_history_pattern = Pattern("remember_history.png")

        restore_firefox_focus()
        new_tab()
        navigate("about:preferences#privacy")
        remember_history_menu_found = False
        scroll_side = find(NavBar.LIBRARY_MENU)
        scroll_side.offset(0, SCREEN_HEIGHT/10)
        click(scroll_side, 1)
        while not remember_history_menu_found:
            remember_history_menu_found = exists(remember_history_pattern, 1)
            scroll(-10)
        assert_true(self, remember_history_menu_found, "History menu found")
