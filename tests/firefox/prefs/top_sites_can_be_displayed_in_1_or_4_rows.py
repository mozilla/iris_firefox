# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='Firefox Home Content - Top Sites can be displayed in 1 or 4 rows',
        test_case_id='161667',
        test_suite_id='2241',
        locale=['en-US'],
        preferences={'devtools.chrome.enabled': True}
    )
    def run(self, firefox):
        about_preferences_home_url_pattern = Pattern('about_preferences_home_url.png')
        home_section_top_sites_four_squares = Pattern('about_preferences_home_top_sites_four_squares.png')
        home_section_top_sites_selected = Pattern('about_preferences_home_top_sites_selected.png').similar(0.97)
        home_section_top_sites_most_visit_default_value = Pattern('home_top_sites_most_visit_default_value.png')
        home_section_top_sites_most_visit_2_row = Pattern('home_top_sites_most_visit_2_row.png')
        home_section_top_sites_most_visit_3_row = Pattern('home_top_sites_most_visit_3_row.png')
        top_sites_section_underneath_search_bar = Pattern('top_sites_section_underneath_search_bar.png')
        browser_console_opened_pattern = Pattern('browser_console_opened.png')
        top_sites_section_resized_browser = Pattern('top_sites_section_resized_browser.png')
        top_sites_section_2_rows = Pattern('top_sites_section_underneath_search_bar_2_row.png')
        top_sites_section_resized_browser_2_rows = Pattern('top_sites_section_resized_browser_2_row.png')
        top_sites_section_3_rows = Pattern('top_sites_section_underneath_search_bar_3_row.png')
        top_sites_section_resized_browser_3_rows = Pattern('top_sites_section_resized_browser_3_row.png')
        top_sites_section_4_rows = Pattern('top_sites_section_underneath_search_bar_4_row.png')
        top_sites_section_resized_browser_4_rows = Pattern('top_sites_section_resized_browser_4_row.png')
        optional_footer_message_from_firefox = Pattern('optional_footer_message_from_firefox.png')
        cross_mark_on_footer_message = Pattern('cross_mark_on_footer_message.png')
        scroll_down_icon = Pattern('scroll_down_icon.png')
        top_sites_section_as_a_reference = Pattern('top_sites_section_as_a_reference.png')

        navigate('about:preferences#home')
        time.sleep(Settings.DEFAULT_UI_DELAY_SHORT)
        about_preferences_home_url_exists = exists(about_preferences_home_url_pattern,
                                                   FirefoxSettings.FIREFOX_TIMEOUT)
        assert about_preferences_home_url_exists, 'Home section of about:preferences page could not loaded successfully'

        # Create Region for top site
        top_site_location = find(top_sites_section_as_a_reference)
        test_search_region = Region(
            top_site_location.x,
            top_site_location.y,
            Screen.SCREEN_WIDTH // 2,
            Screen.SCREEN_HEIGHT // 6,
        )

        # Validate four squares are present before top sites
        top_sites_four_squares_exists = exists(home_section_top_sites_four_squares,
                                               FirefoxSettings.FIREFOX_TIMEOUT,
                                               region=test_search_region)
        assert top_sites_four_squares_exists, 'Four Squares icon is not present beside "Top Sites"'

        # Validate checkbox present before top sites four squares is selected
        home_section_top_sites_selected_exists = exists(home_section_top_sites_selected,
                                                        FirefoxSettings.FIREFOX_TIMEOUT,
                                                        region=test_search_region)
        assert home_section_top_sites_selected_exists, 'Checkbox option present in "Top Sites" is not selected'

        # Validate most visit default value present in top sites drop down
        top_sites_most_visit_default_value_exists = exists(home_section_top_sites_most_visit_default_value,
                                                           FirefoxSettings.FIREFOX_TIMEOUT, region=test_search_region)
        assert top_sites_most_visit_default_value_exists, 'Default number of rows for "Top Sites" is not selected as 1'

        # Top Sites section is displayed underneath the search bar and there are 8 cells displayed in a single row
        # The sites Youtube, Facebook, Amazon, Reddit, Wikipedia and Twitter are listed by default.
        new_tab()
        top_sites_section_underneath_search_bar_exists = exists(top_sites_section_underneath_search_bar,
                                                                FirefoxSettings.FIREFOX_TIMEOUT)
        assert top_sites_section_underneath_search_bar_exists, 'In new tab, 8 cells are not displayed in a single row'

        # if the browser is resized there are only 6 cells and in one row
        open_browser_console()
        browser_console_opened = exists(browser_console_opened_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert browser_console_opened, 'Browser console could not open'

        click(browser_console_opened_pattern)
        paste('window.resizeTo(1000, 700)')
        type(Key.ENTER)

        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

        top_sites_section_resized_browser_exists = exists(top_sites_section_resized_browser,
                                                          FirefoxSettings.FIREFOX_TIMEOUT)
        assert top_sites_section_resized_browser_exists, 'After resizing, 6 cells are not displayed in a single row'

        # change the value from the doorhanger from 1 row to 2 rows.
        maximize_window()
        navigate('about:preferences#home')
        time.sleep(Settings.DEFAULT_UI_DELAY_SHORT)
        click(home_section_top_sites_most_visit_default_value, None, region=test_search_region)
        type(Key.NUM2)
        type(Key.ENTER)

        # The Top Sites section is displayed underneath the search bar and there are 16 cells displayed in 2 rows
        # The sites Youtube, Facebook, Amazon, Reddit, Wikipedia and Twitter are listed by default.
        new_tab()
        top_sites_section_2_rows_exists = exists(top_sites_section_2_rows, FirefoxSettings.FIREFOX_TIMEOUT)
        assert top_sites_section_2_rows_exists, 'In new tab, 16 cells are not displayed in a two rows'

        # if the browser is resized there are 12 cells displayed in 2 rows
        open_browser_console()
        browser_console_opened = exists(browser_console_opened_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert browser_console_opened, 'Browser console could not open'

        click(browser_console_opened_pattern)

        paste('window.resizeTo(1000, 700)')
        type(Key.ENTER)

        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

        top_sites_section_resized_browser_2_rows_exists = exists(top_sites_section_resized_browser_2_rows,
                                                                 FirefoxSettings.FIREFOX_TIMEOUT)
        assert top_sites_section_resized_browser_2_rows_exists, 'After resizing, 12 cells are not displayed in two rows'

        # change the value from the doorhanger from 2 row to 3 rows.
        maximize_window()
        navigate('about:preferences#home')
        click(home_section_top_sites_most_visit_2_row)
        type(Key.NUM3)
        type(Key.ENTER)

        # The Top Sites section is displayed underneath the search bar and there are 24 cells displayed in 3 rows
        # The sites Youtube, Facebook, Amazon, Reddit, Wikipedia and Twitter are listed by default.
        new_tab()
        top_sites_section_3_rows_exists = exists(top_sites_section_3_rows, FirefoxSettings.FIREFOX_TIMEOUT)
        assert top_sites_section_3_rows_exists, 'In new tab, 24 cells are not displayed in a three rows'

        # if the browser is resized there are 18 cells displayed in 3 rows
        open_browser_console()
        browser_console_opened = exists(browser_console_opened_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert browser_console_opened, 'Browser console could not open'
        click(browser_console_opened_pattern)
        paste('window.resizeTo(1000, 700)')
        type(Key.ENTER)

        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

        top_sites_section_resized_browser_3_rows_exists = exists(top_sites_section_resized_browser_3_rows,
                                                                 FirefoxSettings.FIREFOX_TIMEOUT)
        assert top_sites_section_resized_browser_3_rows_exists, 'After resizing, 18 cells are not displayed in three ' \
                                                                'rows '

        # change the value from the doorhanger from 3 row to 4 rows.
        maximize_window()
        navigate('about:preferences#home')
        click(home_section_top_sites_most_visit_3_row)
        type(Key.NUM4)
        type(Key.ENTER)

        # The Top Sites section is displayed underneath the search bar and there are 32 cells displayed in 4 rows
        # The sites Youtube, Facebook, Amazon, Reddit, Wikipedia and Twitter are listed by default.
        new_tab()
        hover(optional_footer_message_from_firefox)
        click(cross_mark_on_footer_message)
        top_sites_section_4_rows_exists = exists(top_sites_section_4_rows, FirefoxSettings.FIREFOX_TIMEOUT)
        assert top_sites_section_4_rows_exists, 'In new tab, 32 cells are not displayed in a four rows'

        # if the browser is resized there are 18 cells displayed in 4 rows
        open_browser_console()
        browser_console_opened = exists(browser_console_opened_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert browser_console_opened, 'Browser console could not open'

        click(browser_console_opened_pattern)

        paste('window.resizeTo(1000, 700)')
        type(Key.ENTER)

        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

        click(scroll_down_icon)
        top_sites_section_resized_browser_4_rows_exists = exists(top_sites_section_resized_browser_4_rows,
                                                                 FirefoxSettings.FIREFOX_TIMEOUT)
        assert top_sites_section_resized_browser_4_rows_exists, 'After resizing, 24 cells are not displayed in four ' \
                                                                'rows '
