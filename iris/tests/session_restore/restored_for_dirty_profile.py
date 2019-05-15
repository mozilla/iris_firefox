
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
        default_zoom_level_toolbar_customize_page_pattern = NavBar.DEFAULT_ZOOM_LEVEL_TOOLBAR_CUSTOMIZE_PAGE
        zoom_controls_customize_page_pattern = NavBar.ZOOM_CONTROLS_CUSTOMIZE_PAGE
        toolbar_pattern = NavBar.TOOLBAR
        hamburger_menu_button_pattern = NavBar.HAMBURGER_MENU.similar(0.95)
        iris_tab_logo_pattern = Pattern('iris_tab.png')
        restore_previous_session_pattern = Pattern('hamburger_restore_previous_session.png')
        firefox_pinned_tab_pattern = Pattern('firefox_pinned_tab.png')

        if not Settings.is_mac():
            hamburger_menu_quit_item_pattern = Pattern('hamburger_menu_exit.png')

        # Define some Location / Region variables
        click_duration = 1
        top_screen_region = Region(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 5)
        bottom_half_region = Screen.BOTTOM_HALF

        iris_tab_logo = exists(iris_tab_logo_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, iris_tab_logo, 'Iris tab available')

        iris_tab_logo_location = find(iris_tab_logo_pattern)
        proper_hamburger_menu_region = Region(0, iris_tab_logo_location.y, SCREEN_WIDTH, SCREEN_HEIGHT // 5)

        hamburger_menu_button_exists = exists(hamburger_menu_button_pattern, Settings.FIREFOX_TIMEOUT,
                                              proper_hamburger_menu_region)
        assert_true(self, hamburger_menu_button_exists, 'Hamburger menu appears on screen.')

        hamburger_menu_button_location = find(hamburger_menu_button_pattern, proper_hamburger_menu_region)

        click(hamburger_menu_button_location, click_duration)

        restore_previous_session_exists = exists(restore_previous_session_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, restore_previous_session_exists, '\'Restore previous session\' item located')

        restore_previous_session_location = find(restore_previous_session_pattern)

        if not Settings.is_mac():
            hamburger_menu_quit_displayed = exists(hamburger_menu_quit_item_pattern, Settings.FIREFOX_TIMEOUT)
            assert_true(self, hamburger_menu_quit_displayed, 'Close Firefox from the \'Hamburger\' menu.')

            hamburger_menu_quit_item_location = find(hamburger_menu_quit_item_pattern)

        restore_firefox_focus()

        #  Step 2: Customize Firefox: change few buttons position

        zoom_indicator_not_displayed = exists(NavBar.DEFAULT_ZOOM_LEVEL_TOOLBAR_CUSTOMIZE_PAGE, Settings.TINY_FIREFOX_TIMEOUT, top_screen_region)
        assert_false(self, zoom_indicator_not_displayed, 'Zoom indicator not displayed by default in the URL bar.')

        click_hamburger_menu_option('Customize...')

        zoom_controls_customize_exists = exists(zoom_controls_customize_page_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, zoom_controls_customize_exists, 'Zoom controls found in the \'Customize\' page.')

        drag_drop(zoom_controls_customize_page_pattern, toolbar_pattern, click_duration)
        time.sleep(Settings.UI_DELAY)
        reset_mouse()

        zoom_toolbar_dragged = exists(default_zoom_level_toolbar_customize_page_pattern, Settings.SITE_LOAD_TIMEOUT,
                                      top_screen_region)
        assert_true(self, zoom_toolbar_dragged, 'Zoom controls successfully dragged and dropped in toolbar.')

        close_customize_page()

        # Pin tab

        navigate(LocalWeb.FIREFOX_TEST_SITE)

        firefox_tab_opened = exists(firefox_tab_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, firefox_tab_opened, 'Firefox webpage is opened')

        right_click(firefox_tab_pattern, Settings.TINY_FIREFOX_TIMEOUT)

        unpinned_dropdown_opened = exists(pin_tab_pattern)
        assert_true(self, unpinned_dropdown_opened, 'Tab dropdown menu opened')

        click(pin_tab_pattern)

        second_tab_pinned = exists(firefox_pinned_tab_pattern)
        assert_true(self, second_tab_pinned, 'Firefox tab is pinned')

        # open several different websites
        local_url = [LocalWeb.FOCUS_TEST_SITE, LocalWeb.MOZILLA_TEST_SITE]
        local_url_logo_pattern = [LocalWeb.FOCUS_LOGO, LocalWeb.MOZILLA_LOGO]

        for _ in range(2):
            new_tab()
            navigate(local_url[_])
            website_loaded = exists(local_url_logo_pattern[_], Settings.SITE_LOAD_TIMEOUT)
            assert_true(self, website_loaded, 'Website {0} loaded' .format(_ + 1))

        # Customize Firefox: set a theme, change a few button position, pin a tab, etc.
        click_hamburger_menu_option('Customize...')

        theme_button_available = exists(Customize.THEMES_DEFAULT_SET, Settings.FIREFOX_TIMEOUT, bottom_half_region)
        assert_true(self, theme_button_available, 'Themes button is available.')

        click(Customize.THEMES_DEFAULT_SET)

        dark_theme_option_available = exists(Customize.DARK_THEME_OPTION, Settings.FIREFOX_TIMEOUT, bottom_half_region)
        assert_true(self, dark_theme_option_available, 'Dark theme option is available.')

        click(Customize.DARK_THEME_OPTION)

        dark_theme_is_set = exists(Customize.DARK_THEME_SET, Settings.FIREFOX_TIMEOUT, bottom_half_region)
        assert_true(self, dark_theme_is_set, 'Dark theme is set.')

        close_customize_page()

        # Quit via Hamburger menu
        if Settings.is_mac():
            type('q', KeyModifier.CMD)

        else:
            click(hamburger_menu_button_location, click_duration)

            click(hamburger_menu_quit_item_location, click_duration)

        restart_firefox(self, self.browser.path, self.profile_path, 'about:home',
                        image=NavBar.HAMBURGER_MENU_DARK_THEME)

        time.sleep(Settings.SHORT_FIREFOX_TIMEOUT)  # wait while Linux maximizes window

        hamburger_menu_button_exists = exists(NavBar.HAMBURGER_MENU_DARK_THEME, Settings.FIREFOX_TIMEOUT)
        assert_true(self, hamburger_menu_button_exists, 'The Hamburger menu is successfully displayed.')

        click(NavBar.HAMBURGER_MENU_DARK_THEME, click_duration)

        click(restore_previous_session_location, Settings.TINY_FIREFOX_TIMEOUT)

        select_tab(1)

        firefox_page_content_restored = exists(LocalWeb.FIREFOX_LOGO)
        assert_true(self, firefox_page_content_restored, 'Firefox pinned tab restored successfully.')

        select_tab(2)

        focus_tab_restored = exists(LocalWeb.FOCUS_LOGO)
        assert_true(self, focus_tab_restored, 'Focus tab restored successfully.')

        select_tab(3)

        mozilla_tab_restored = exists(LocalWeb.MOZILLA_LOGO)
        assert_true(self, mozilla_tab_restored, 'Mozilla tab restored successfully.\nThe previous session is '
                                                'successfully restored (All previously closed tabs are successfully'
                                                'restored).')
