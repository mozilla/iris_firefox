# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Scroll position is saved in each window'
        self.test_case_id = '114827'
        self.test_suite_id = '68'
        self.locales = ['en-US']

    def run(self):
        hamburger_menu_button_pattern = NavBar.HAMBURGER_MENU.similar(0.95)
        firefox_test_site_tab_pattern = Pattern('firefox_tab_icon_text.png')
        focus_test_site_tab_pattern = Pattern('focus_tab_icon_text.png')
        restore_previous_session_pattern = Pattern('hamburger_restore_previous_session.png')
        firefox_tab_scrolled_pattern = Pattern('firefox_tab_scrolled.png')
        focus_tab_scrolled_pattern = Pattern('focus_tab_scrolled.png')
        browser_console_title_pattern = Pattern('browser_console_title.png')
        browser_console_empty_line_pattern = Pattern('browser_console_empty_line.png')
        iris_tab_logo_pattern = Pattern('iris_tab.png')

        if not Settings.is_mac():
            hamburger_menu_quit_item_pattern = Pattern('hamburger_menu_exit.png')

        iris_tab_logo = exists(iris_tab_logo_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, iris_tab_logo, 'Iris tab available')
        iris_tab_logo_location = find(iris_tab_logo_pattern)
        proper_hamburger_menu_region = Region(0, iris_tab_logo_location.y, width=SCREEN_WIDTH, height=SCREEN_HEIGHT/4)

        change_preference('devtools.chrome.enabled', True)

        if not Settings.is_mac():
            minimize_window()

        open_browser_console()
        browser_console_opened = exists(browser_console_title_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, browser_console_opened, 'Browser console opened.')
        paste('window.resizeTo(800, 450)')
        type(Key.ENTER)

        browser_console_empty_line = exists(browser_console_empty_line_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, browser_console_empty_line, 'Value entered in browser console.')

        if not Settings.is_mac():
            click_window_control('close')
        else:
            type('w', KeyModifier.CMD)

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)

        tab_one_loaded = exists(LocalWeb.FIREFOX_LOGO, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, tab_one_loaded, 'Firefox tab loaded')

        firefox_tab_is_active = exists(firefox_test_site_tab_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, firefox_tab_is_active, 'Firefox tab is active.')

        tab_width, tab_height = firefox_test_site_tab_pattern.get_size()
        firefox_tab_location_before = find(firefox_test_site_tab_pattern)
        firefox_tab_region_before = Region(firefox_tab_location_before.x-tab_width, 0,
                                           width=tab_width*3, height=SCREEN_HEIGHT)
        firefox_tab_region_after = Region((SCREEN_WIDTH/2)-tab_width, 0, width=tab_width*3, height=SCREEN_HEIGHT)

        new_tab()
        navigate(LocalWeb.FOCUS_TEST_SITE)

        tab_two_loaded = exists(LocalWeb.FOCUS_LOGO, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, tab_two_loaded, 'Focus tab loaded')

        focus_test_site_tab_exists = exists(focus_test_site_tab_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, focus_test_site_tab_exists, 'Focus site tab is active.')

        focus_tab_location_before = find(focus_test_site_tab_pattern)
        focus_tab_region_before = Region(0, focus_tab_location_before.y-(tab_height/2),
                                         width=SCREEN_WIDTH, height=tab_height*2)
        focus_tab_region_after = Region(0, (SCREEN_HEIGHT/2)-tab_height*5, width=SCREEN_WIDTH, height=tab_height*10)

        # Drag-n-drop Focus tab
        focus_tab_drop_location = Location(x=50, y=(SCREEN_HEIGHT / 2))
        drag_drop(focus_tab_location_before, focus_tab_drop_location)

        try:
            focus_tab_dragged = wait_vanish(focus_test_site_tab_pattern, DEFAULT_FIREFOX_TIMEOUT,
                                            focus_tab_region_before)
            assert_true(self, focus_tab_dragged, 'Focus tab dragged.')
        except FindError:
            raise FindError('Focus tab was not dragged out.')

        focus_tab_dropped = exists(focus_test_site_tab_pattern, DEFAULT_FIREFOX_TIMEOUT,
                                   in_region=focus_tab_region_after)
        assert_true(self, focus_tab_dropped, 'Focus tab dropped.')

        focus_content_exists = exists(LocalWeb.FOCUS_LOGO, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, focus_content_exists, 'Focus content before scrolling is on the page.')
        click(focus_test_site_tab_pattern.target_offset(0, 100))
        repeat_key_down(5)

        focus_tab_scrolled = exists(focus_tab_scrolled_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, focus_tab_scrolled, 'Focus tab scrolled successful.')

        # Drag-n-drop Firefox tab
        firefox_tab_drop_location = Location(x=SCREEN_WIDTH/2, y=tab_height*4)
        drag_drop(firefox_tab_location_before, firefox_tab_drop_location)

        try:
            firefox_test_site_tab_dragged = wait_vanish(firefox_test_site_tab_pattern, DEFAULT_FIREFOX_TIMEOUT,
                                                        firefox_tab_region_before)
            assert_true(self, firefox_test_site_tab_dragged, 'Firefox tab dragged.')
        except FindError:
            raise FindError('Firefox tab was not dragged out.')

        firefox_tab_dropped = exists(firefox_test_site_tab_pattern, DEFAULT_FIREFOX_TIMEOUT,
                                     in_region=firefox_tab_region_after)
        assert_true(self, firefox_tab_dropped, 'Firefox tab dropped.')

        firefox_content_exists = exists(LocalWeb.FIREFOX_LOGO, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, firefox_content_exists, 'Firefox content before scrolling is on the page.')
        click(firefox_test_site_tab_pattern.target_offset(0, 100))
        repeat_key_down(5)

        firefox_tab_scrolled = exists(firefox_tab_scrolled_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, firefox_tab_scrolled, 'Firefox tab scrolled successful.')

        # Quit via Hamburger menu
        hamburger_menu_button_exists = exists(hamburger_menu_button_pattern, DEFAULT_FIREFOX_TIMEOUT,
                                              in_region=proper_hamburger_menu_region)
        assert_true(self, hamburger_menu_button_exists, 'Hamburger menu appears on screen.')

        if not Settings.is_mac():
            click(hamburger_menu_button_pattern, DEFAULT_UI_DELAY, in_region=proper_hamburger_menu_region)
            hamburger_menu_quit_displayed = exists(hamburger_menu_quit_item_pattern, DEFAULT_FIREFOX_TIMEOUT)
            assert_true(self, hamburger_menu_quit_displayed, 'Close Firefox from the "Hamburger" menu.')
            click(hamburger_menu_quit_item_pattern, DEFAULT_UI_DELAY)
        else:
            type('q', KeyModifier.CMD)

        #  firefox_runner = None to prevent automatic restore of previous session
        status = self.firefox_runner.process_handler.wait(Settings.FIREFOX_TIMEOUT)
        if status is None:
            self.firefox_runner.stop()
            self.firefox_runner = None

        # keyboard shortcut of method restart_firefox() can break test
        self.firefox_runner = launch_firefox(self.browser.path, self.profile_path, self.base_local_web_url)
        self.firefox_runner.start()

        iris_tab_logo = exists(iris_tab_logo_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, iris_tab_logo, 'Iris tab available')
        iris_tab_logo_location = find(iris_tab_logo_pattern)
        proper_hamburger_menu_region = Region(0, iris_tab_logo_location.y, width=SCREEN_WIDTH, height=200)

        hamburger_menu_button_exists = exists(hamburger_menu_button_pattern, DEFAULT_FIREFOX_TIMEOUT,
                                              in_region=proper_hamburger_menu_region)
        assert_true(self, hamburger_menu_button_exists, 'Hamburger menu appears on screen.', )
        click(NavBar.HAMBURGER_MENU, in_region=proper_hamburger_menu_region)

        restore_previous_session_exists = exists(restore_previous_session_pattern, DEFAULT_FIREFOX_TIMEOUT)

        assert_true(self, restore_previous_session_exists, '"Restore previous session" item located')
        click(restore_previous_session_pattern)

        # Firefox tab restored
        firefox_tab_exists = exists(firefox_test_site_tab_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, firefox_tab_exists, 'Firefox tab exists after restart.')

        firefox_tab_restarted = exists(firefox_test_site_tab_pattern)
        assert_true(self, firefox_tab_restarted, 'Firefox window is restored and ')

        firefox_top_content_not_exists = not exists(LocalWeb.FIREFOX_LOGO)
        assert_true(self, firefox_top_content_not_exists, 'top content is not on screen,')
        firefox_tab_scrolled_content_exists = exists(firefox_tab_scrolled_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, firefox_tab_scrolled_content_exists, 'tab content is scrolled.')

        close_tab()

        # Focus tab restored
        focus_test_site_tab_exists = exists(focus_test_site_tab_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, focus_test_site_tab_exists, 'Focus tab exists after restart.')

        focus_tab_restarted = exists(focus_test_site_tab_pattern)
        assert_true(self, focus_tab_restarted, 'Focus window is restored and ')

        focus_top_content_not_exists = not exists(LocalWeb.FOCUS_LOGO)
        assert_true(self, focus_top_content_not_exists, 'top content is not on screen,')

        focus_tab_scrolled_content_exists = exists(focus_tab_scrolled_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, focus_tab_scrolled_content_exists, ' tab content is scrolled.')

        close_tab()
        close_tab()