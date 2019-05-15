
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Previous session can be restored for a dirty profile'
        self.test_case_id = '3945'
        self.test_suite_id = '68'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.set_profile_pref({'browser.startup.homepage': 'about:home'})
        self.profile = Profile.TEN_BOOKMARKS

    def run(self):
        firefox_tab_pattern = Pattern('firefox_tab.png')
        pin_tab_pattern = Pattern('pin_tab_item.png')
        firefox_pinned_tab_pattern = Pattern('firefox_pinned_tab.png')
        default_zoom_level_toolbar_customize_page_pattern = NavBar.DEFAULT_ZOOM_LEVEL_TOOLBAR_CUSTOMIZE_PAGE
        zoom_controls_customize_page_pattern = NavBar.ZOOM_CONTROLS_CUSTOMIZE_PAGE
        url_bar_default_zoom_level_pattern = LocationBar.URL_BAR_DEFAULT_ZOOM_LEVEL
        toolbar_pattern = NavBar.TOOLBAR
        hamburger_menu_button_pattern = NavBar.HAMBURGER_MENU.similar(0.95)
        iris_tab_logo_pattern = Pattern('iris_tab.png')
        restore_previous_session_pattern = Pattern('hamburger_restore_previous_session.png')

        hamburger_menu_quit_item_pattern = None
        if not Settings.is_mac():
            hamburger_menu_quit_item_pattern = Pattern('hamburger_menu_exit.png')

        # Define some Location / Region variables
        top_screen_region = Region(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 5)

        iris_tab_logo = exists(iris_tab_logo_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, iris_tab_logo, 'Iris tab available')

        iris_tab_logo_location = find(iris_tab_logo_pattern)
        proper_hamburger_menu_region = Region(0, iris_tab_logo_location.y, width=SCREEN_WIDTH, height=SCREEN_HEIGHT//5)

        hamburger_menu_button_exists = exists(hamburger_menu_button_pattern, Settings.FIREFOX_TIMEOUT,
                                              in_region=proper_hamburger_menu_region)
        assert_true(self, hamburger_menu_button_exists, 'Hamburger menu appears on screen.')

        hamburger_menu_button_location = find(hamburger_menu_button_pattern, proper_hamburger_menu_region)

        click(hamburger_menu_button_location, 1)

        restore_previous_session_exists = exists(restore_previous_session_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, restore_previous_session_exists, '"Restore previous session" item located')

        restore_previous_session_location = find(restore_previous_session_pattern)

        #  Step 2: change few buttons position

        navigate(LocalWeb.FIREFOX_TEST_SITE)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        region = top_screen_region
        expected = region.exists(url_bar_default_zoom_level_pattern, 10)
        assert_true(self, expected, 'Zoom indicator not displayed by default in the url bar.')

        click_hamburger_menu_option('Customize...')

        expected = exists(zoom_controls_customize_page_pattern, 10)
        assert_true(self, expected, 'Zoom controls found in the \'Customize\' page.')

        drag_drop(zoom_controls_customize_page_pattern, toolbar_pattern, 0.5)
        time.sleep(Settings.UI_DELAY)
        reset_mouse()

        expected = exists(default_zoom_level_toolbar_customize_page_pattern, 10,
                          in_region=Region(0, 0, SCREEN_WIDTH, 300))
        assert_true(self, expected, 'Zoom controls successfully dragged and dropped in toolbar.')

        close_customize_page()

        # Pin tab

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)

        firefox_tab_opened = exists(firefox_tab_pattern)
        assert_true(self, firefox_tab_opened, 'Second webpage is opened')
        right_click(firefox_tab_pattern)

        unpinned_dropdown_opened = exists(pin_tab_pattern)
        assert_true(self, unpinned_dropdown_opened, 'Dropdown for common tab opened')
        click(pin_tab_pattern)

        second_tab_pinned = exists(firefox_pinned_tab_pattern)
        assert_true(self, second_tab_pinned, 'Second tab is pinned')

        # open several different website
        local_url = [LocalWeb.FOCUS_TEST_SITE, LocalWeb.MOZILLA_TEST_SITE]
        local_url_logo_pattern = [LocalWeb.FOCUS_LOGO, LocalWeb.MOZILLA_LOGO]

        for _ in range(2):
            new_tab()
            navigate(local_url[_])
            website_loaded = exists(local_url_logo_pattern[_], 20)
            assert_true(self, website_loaded,
                        'Website {0} loaded'
                        .format(_ + 1))

        close_tab()

        one_tab_exists = exists(local_url_logo_pattern[0], 20)
        assert_true(self, one_tab_exists,
                    'One opened tab left. {0} tabs were successfully closed.'
                    .format(len(local_url) - 1))

        undo_close_tab()
        tab_is_restored = exists(local_url_logo_pattern[1])  # +1 as url[0] is one opened tab
        assert_true(self, tab_is_restored,
                    'Tab successfully restored')

        # Customize Firefox: set a theme, change a few button position, pin a tab, etc.
        click_hamburger_menu_option('Customize...')

        region_bottom_half = Screen.BOTTOM_HALF

        expected = region_bottom_half.exists(Customize.THEMES_DEFAULT_SET, 10)
        assert_true(self, expected, 'Themes button is available.')

        click(Customize.THEMES_DEFAULT_SET)

        expected = region_bottom_half.exists(Customize.DARK_THEME_OPTION, 10)
        assert_true(self, expected, 'Dark theme option is available.')

        click(Customize.DARK_THEME_OPTION)

        expected = region_bottom_half.exists(Customize.DARK_THEME_SET, 10)
        assert_true(self, expected, 'Dark theme is set.')

        close_customize_page()

        # Quit via Hamburger menu
        if Settings.is_mac():
            type('q', KeyModifier.CMD)

        else:
            click(hamburger_menu_button_location, DEFAULT_UI_DELAY)

            hamburger_menu_quit_displayed = exists(hamburger_menu_quit_item_pattern, DEFAULT_FIREFOX_TIMEOUT)
            assert_true(self, hamburger_menu_quit_displayed, 'Close Firefox from the "Hamburger" menu.')

            click(hamburger_menu_quit_item_pattern, DEFAULT_UI_DELAY)

        restart_firefox(self,
                        self.browser.path,
                        self.profile_path,
                        'about:home', image=NavBar.HAMBURGER_MENU_DARK_THEME)

        click(NavBar.HAMBURGER_MENU_DARK_THEME, 1)

        click(restore_previous_session_location, 1)

        time.sleep(1234)