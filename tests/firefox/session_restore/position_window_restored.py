# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Width, height and position of each window are restored.',
        test_case_id='114826',
        test_suite_id='68',
        locales=Locales.ENGLISH
    )
    def run(self, firefox):
        firefox_test_site_tab_pattern = Pattern('firefox_test_site_tab.png').similar(0.9)
        focus_test_site_tab_pattern = Pattern('focus_test_site_tab.png').similar(0.9)
        restore_previous_session_pattern = Pattern('restore_previous_session_item.png')
        console_output_height_500 = Pattern('console_output_height_500.png')
        console_output_height_400 = Pattern('console_output_height_400.png')
        console_output_width_1000 = Pattern('console_output_width_1000.png')
        console_output_width_500 = Pattern('console_output_width_500.png')
        console_output_width_600 = Pattern('console_output_width_600.png')

        hamburger_menu_quit_item_pattern = None
        if not OSHelper.is_mac():
            hamburger_menu_quit_item_pattern = Pattern('hamburger_menu_quit_item.png').similar(0.9)

        iris_icon_height = LocalWeb.IRIS_LOGO_ACTIVE_TAB.get_size()[1]
        click_duration = 1
        iris_tab_offset = - iris_icon_height

        iris_tab_displayed = exists(LocalWeb.IRIS_LOGO_ACTIVE_TAB)
        assert iris_tab_displayed, 'Iris tab is displayed properly'

        if OSHelper.is_linux():
            iris_tab_offset = find(LocalWeb.IRIS_LOGO).y

        if not OSHelper.is_mac():
            minimize_window()

        default_window_location = Location(x=(Screen.SCREEN_WIDTH / 10), y=(Screen.SCREEN_HEIGHT / 20))

        if OSHelper.is_linux():
            default_window_location.offset(iris_tab_offset, 0)

        iris_tab_on_start_position = find(LocalWeb.IRIS_LOGO_ACTIVE_TAB)
        iris_tab_on_start_position.offset(iris_tab_offset, 0)

        drag_drop(iris_tab_on_start_position, default_window_location, duration=click_duration)

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)
        tab_one_loaded = exists(firefox_test_site_tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert tab_one_loaded, 'First tab loaded'

        new_tab()
        navigate(LocalWeb.FOCUS_TEST_SITE)
        tab_two_loaded = exists(focus_test_site_tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert tab_two_loaded, 'Second tab loaded'

        open_browser_console()
        paste('window.resizeTo(1000, 400)')
        type(Key.ENTER)

        close_tab()

        tabs_located_after_size_changed = exists(focus_test_site_tab_pattern)
        assert tabs_located_after_size_changed, 'Tabs located after size of main window had changed.'

        default_tabs_position = find(focus_test_site_tab_pattern)

        click(default_tabs_position)

        default_tabs_region = Region(0, default_tabs_position.y, width=Screen.SCREEN_WIDTH,
                                     height=Screen.SCREEN_HEIGHT / 10)

        tab_two_drop_location = Location(x=0, y=(default_tabs_position.y + 2 * Screen.SCREEN_HEIGHT / 5))

        drag_drop(default_tabs_position, tab_two_drop_location, duration=click_duration)

        focus_page_content_displayed = exists(LocalWeb.FOCUS_LOGO)
        assert focus_page_content_displayed, 'Focus webpage content is being displayed'

        click(LocalWeb.FOCUS_LOGO)

        open_browser_console()
        paste('window.resizeTo(600, 400)')
        type(Key.ENTER)
        close_tab()

        tab_two_relocated = not exists(focus_test_site_tab_pattern, region=default_tabs_region)
        active_tab_switched = exists(firefox_test_site_tab_pattern)
        assert tab_two_relocated and active_tab_switched, 'Second tab relocated'

        tab_one_location = find(firefox_test_site_tab_pattern)

        click(tab_one_location)

        tab_one_drop_location = Location(x=(tab_one_location.x + Screen.SCREEN_WIDTH / 5),
                                         y=(tab_one_location.y + Screen.SCREEN_HEIGHT / 10))

        drag_drop(tab_one_location, tab_one_drop_location, duration=click_duration)

        firefox_page_displayed = exists(LocalWeb.FIREFOX_LOGO)
        assert firefox_page_displayed, 'Firefox webpage content is being displayed'

        click(LocalWeb.FIREFOX_LOGO)

        open_browser_console()
        paste('window.resizeTo(500, 500)')
        type(Key.ENTER)
        close_tab()

        tab_one_drop_location.offset(Screen.SCREEN_WIDTH / 10, Screen.SCREEN_HEIGHT / 20)
        tab_one_moved = exists(firefox_test_site_tab_pattern)

        assert tab_one_moved, 'Changes to height and width performed. First tab\'s first relocation completed.'
        tab_one_intermediate_location = find(firefox_test_site_tab_pattern)

        if not OSHelper.is_linux():
            tab_one_intermediate_location.offset(-iris_icon_height, 0)
        else:
            tab_one_region = Region(tab_one_intermediate_location.x, tab_one_intermediate_location.y,
                                    Screen.SCREEN_WIDTH * 2 // 3, Screen.SCREEN_HEIGHT // 2)

            hamburger_menu_in_tab_one_found = exists(NavBar.HAMBURGER_MENU, region=tab_one_region)
            assert hamburger_menu_in_tab_one_found, 'Hamburger menu button of first tab window is found'

            hamburger_menu_button_location_x = find(NavBar.HAMBURGER_MENU, region=tab_one_region).x
            tab_one_drag_drop_offset = hamburger_menu_button_location_x - tab_one_intermediate_location.x
            tab_one_intermediate_location.offset(tab_one_drag_drop_offset, 0)
            tab_one_drop_location.offset(tab_one_drag_drop_offset, 0)

        drag_drop(tab_one_intermediate_location, tab_one_drop_location, duration=click_duration)

        tab_one_relocated = not exists(firefox_test_site_tab_pattern, region=default_tabs_region)
        assert tab_one_relocated, 'First opened tab relocated. Two tabs were dragged outside the main browser window.'

        tab_one_moved_twice = exists(firefox_test_site_tab_pattern)
        assert tab_one_moved_twice, 'Tabs positioned in different places.'

        if not OSHelper.is_mac():

            click(NavBar.HAMBURGER_MENU, click_duration)

            hamburger_menu_quit_displayed = exists(hamburger_menu_quit_item_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            assert hamburger_menu_quit_displayed, 'Close Firefox from the "Hamburger" menu.'
            click(hamburger_menu_quit_item_pattern, click_duration)
        else:
            quit_firefox()

        firefox.restart()

        firefox_restarted = exists(NavBar.HAMBURGER_MENU.similar(0.9), FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert firefox_restarted, 'Firefox restarted successfully'

        click(NavBar.HAMBURGER_MENU, duration=click_duration)

        restore_previous_session_located = exists(restore_previous_session_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert restore_previous_session_located, \
            'The "Hamburger" menu is successfully displayed. "Restore previous session" menu item located'

        click(restore_previous_session_pattern, click_duration)

        focus_site_restored = exists(focus_test_site_tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert focus_site_restored, 'Firefox window with Focus webpage is opened'

        firefox_test_site_restored = exists(firefox_test_site_tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert firefox_test_site_restored, 'Firefox window with Focus webpage is opened'

        iris_page_restored = exists(LocalWeb.IRIS_LOGO_INACTIVE_TAB, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert iris_page_restored, 'Firefox window with Iris webpage is opened'

        firefox_test_site_restored_position = find(firefox_test_site_tab_pattern)
        focus_site_restored_position = find(focus_test_site_tab_pattern)
        iris_tab_restored_position = find(LocalWeb.IRIS_LOGO_ACTIVE_TAB)

        firefox_test_site_most_right = firefox_test_site_restored_position.x > max(iris_tab_restored_position.x,
                                                                                   focus_site_restored_position.x)

        firefox_test_site_middle_height = focus_site_restored_position.y > max(firefox_test_site_restored_position.y,
                                                                               iris_tab_restored_position.y)

        focus_site_the_lowest = focus_site_restored_position.y > max(iris_tab_restored_position.y,
                                                                     firefox_test_site_restored_position.y)

        focus_site_most_left = focus_site_restored_position.x <= iris_tab_restored_position.x

        assert firefox_test_site_most_right and firefox_test_site_middle_height, \
            'First restored window is located in the right position'

        assert focus_site_most_left, 'Second window is the most left'
        assert focus_site_the_lowest, 'Second restored window is located in the right position'

        click(firefox_test_site_tab_pattern, click_duration)

        open_browser_console()
        paste('window.innerHeight')
        type(Key.ENTER)
        test_site_window_height_matched = exists(console_output_height_500)

        paste('window.innerWidth')
        type(Key.ENTER)

        test_site_window_width_matched = exists(console_output_width_500)
        assert test_site_window_width_matched and test_site_window_height_matched, 'First window size matched'
        close_tab()

        click(focus_test_site_tab_pattern, click_duration)

        open_browser_console()
        paste('window.innerHeight')
        type(Key.ENTER)
        focus_site_window_height_matched = exists(console_output_height_400)

        paste('window.innerWidth')
        type(Key.ENTER)
        focus_site_window_width_matched = exists(console_output_width_600)
        assert focus_site_window_height_matched and focus_site_window_width_matched, 'Second window size matched'

        close_tab()

        click(LocalWeb.IRIS_LOGO_ACTIVE_TAB, click_duration)

        open_browser_console()

        paste('window.innerHeight')
        type(Key.ENTER)
        iris_window_height_matched = exists(console_output_height_400)

        paste('window.innerWidth')
        type(Key.ENTER)
        iris_window_width_matched = exists(console_output_width_1000)

        assert iris_window_height_matched and iris_window_width_matched, \
            'Iris window size matched. The previous session is successfully restored and the ' \
            'width, height and position of each tab is displayed as in the previous session.'

        close_tab()

        close_window()
        close_window()
