from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Scroll position is saved in each window'
        self.test_case_id = '114827'
        self.test_suite_id = '68'
        self.locales = ['en-US']

    def run(self):
        firefox_test_site_tab_pattern = Pattern("firefox_test_site_tab.png")
        focus_test_site_tab_pattern = Pattern("focus_test_site_tab.png")
        firefox_tab_scrolled_pattern = Pattern("firefox_tab_scrolled.png")
        focus_tab_scrolled_pattern = Pattern("focus_tab_scrolled.png")
        hamburger_menu_button_pattern = NavBar.HAMBURGER_MENU

        if not Settings.is_mac():
            hamburger_menu_quit_item_pattern = Pattern('hamburger_menu_quit_item.png')

        change_preference("devtools.chrome.enabled", True)

        if not Settings.is_mac():
            minimize_window()

        open_browser_console()
        time.sleep(DEFAULT_SYSTEM_DELAY)
        paste("window.resizeTo(800, 450)")
        time.sleep(DEFAULT_SYSTEM_DELAY)
        type(Key.ENTER)

        if not Settings.is_mac():
            click_window_control('close')
        else:
            type('w', KeyModifier.CMD)

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)

        tab_one_loaded = exists(LocalWeb.FIREFOX_LOGO, 20)
        assert_true(self, tab_one_loaded, "First tab loaded")
        firefox_tab_location_before = find(firefox_test_site_tab_pattern)

        new_tab()
        navigate(LocalWeb.FOCUS_TEST_SITE)

        tab_two_loaded = exists(LocalWeb.FOCUS_LOGO, 20)
        assert_true(self, tab_two_loaded, "Second tab loaded")
        focus_tab_location_before = find(focus_test_site_tab_pattern)

        focus_test_site_tab_exists = exists(focus_test_site_tab_pattern, 20)
        assert_true(self, focus_test_site_tab_exists, 'Focus site tab is active.')

        # Drag-n-drop Focus tab
        focus_tab_drop_location = Location(x=50,
                                           y=(SCREEN_HEIGHT / 2))

        drag_drop(focus_tab_location_before, focus_tab_drop_location, duration=0.5)

        focus_content_exists = exists(LocalWeb.FOCUS_LOGO)
        assert_true(self, focus_content_exists, 'Focus content is visible.')

        click(LocalWeb.FOCUS_LOGO)
        repeat_key_down(5)

        focus_tab_scrolled = exists(focus_tab_scrolled_pattern, 20)
        assert_true(self, focus_tab_scrolled, 'Focus tab scrolled.')

        focus_test_site_tab_exists = exists(focus_test_site_tab_pattern, 20)
        assert_true(self, focus_test_site_tab_exists, 'Focus tab exists after drag-n-drop.')

        # Drag-n-drop Firefox tab
        firefox_tab_drop_location = Location(x=(SCREEN_WIDTH / 2),
                                             y=50)

        drag_drop(firefox_tab_location_before, firefox_tab_drop_location, duration=0.5)

        firefox_content_exists = exists(LocalWeb.FIREFOX_LOGO)
        assert_true(self, firefox_content_exists, 'Firefox content is visible.')

        click(LocalWeb.FIREFOX_LOGO)
        repeat_key_down(5)

        firefox_tab_scrolled = exists(firefox_tab_scrolled_pattern, 20)
        assert_true(self, firefox_tab_scrolled, 'Firefox tab scrolled.')

        firefox_tab_exists = exists(firefox_test_site_tab_pattern, 20)
        assert_true(self, firefox_tab_exists, 'Firefox tab is active.')

        time.sleep(DEFAULT_UI_DELAY)

        if Settings.is_mac():
            type('q', KeyModifier.CMD)
        else:
            hamburger_menu_button_exists = exists(hamburger_menu_button_pattern, 20)
            assert_true(self, hamburger_menu_button_exists, 'Hamburger button exists.')
            click(hamburger_menu_button_pattern)

            hamburger_menu_quit_item_exists = exists(hamburger_menu_quit_item_pattern, 20)
            assert_true(self, hamburger_menu_quit_item_exists, 'Hamburger menu exit item exists.')
            click(hamburger_menu_quit_item_pattern)

        restart_firefox(self,
                        self.browser.path,
                        self.profile_path,
                        self.base_local_web_url)

        if Settings.is_linux():
            click_window_control('maximize')

        click_hamburger_menu_option("Restore Previous Session")
        time.sleep(DEFAULT_SYSTEM_DELAY)

        firefox_tab_exists = exists(firefox_test_site_tab_pattern, 20)
        assert_true(self, firefox_tab_exists, 'Firefox tab exists after restart.')

        firefox_tab_restarted = exists(firefox_test_site_tab_pattern)
        assert_true(self, firefox_tab_restarted, 'Firefox window is restored and ')

        firefox_top_content_not_exists = not exists(LocalWeb.FIREFOX_LOGO)
        assert_true(self, firefox_top_content_not_exists, 'top content is not on screen,')
        firefox_tab_scrolled_content_exists = exists(firefox_tab_scrolled_pattern, 20)
        assert_true(self, firefox_tab_scrolled_content_exists, 'tab content is scrolled.')

        close_tab()

        focus_test_site_tab_exists = exists(focus_test_site_tab_pattern, 20)
        assert_true(self, focus_test_site_tab_exists, 'Focus tab exists after restart.')

        focus_tab_restarted = exists(focus_test_site_tab_pattern)
        assert_true(self, focus_tab_restarted, 'Focus window is restored and ')

        focus_top_content_not_exists = not exists(LocalWeb.FOCUS_LOGO)
        assert_true(self, focus_top_content_not_exists, 'top content is not on screen, ')

        focus_tab_scrolled_content_exists = exists(focus_tab_scrolled_pattern, 20)
        assert_true(self, focus_tab_scrolled_content_exists, 'tab content is scrolled.')

        close_tab()
