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
        wait(about_preferences_home_url_pattern)
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

        top_sites_four_squares_exists = exists(home_section_top_sites_four_squares,
                                               FirefoxSettings.FIREFOX_TIMEOUT,
                                               region=test_search_region)
        assert top_sites_four_squares_exists, 'Four Squares icon is not present beside "Top Sites"'

        home_section_top_sites_selected_exists = exists(home_section_top_sites_selected,
                                                        FirefoxSettings.FIREFOX_TIMEOUT,
                                                        region=test_search_region)
        assert home_section_top_sites_selected_exists, 'Checkbox option present in "Top Sites" is not selected'

        top_sites_most_visit_default_value_exists = exists(home_section_top_sites_most_visit_default_value,
                                                           FirefoxSettings.FIREFOX_TIMEOUT, region=test_search_region)
        assert top_sites_most_visit_default_value_exists, 'Default number of rows for "Top Sites" is not selected as 1'

        new_tab()
        top_sites_section_underneath_search_bar_exists = exists(top_sites_section_underneath_search_bar,
                                                                FirefoxSettings.FIREFOX_TIMEOUT)
        assert top_sites_section_underneath_search_bar_exists, 'In new tab, 8 cells are not displayed in a single row'

        self.resize_browser('1000', '700')
        top_sites_section_resized_browser_exists = exists(top_sites_section_resized_browser,
                                                          FirefoxSettings.FIREFOX_TIMEOUT)
        assert top_sites_section_resized_browser_exists, 'After resizing, 6 cells are not displayed in a single row'

        self.top_site_dropdown(home_section_top_sites_most_visit_default_value, test_search_region, Key.NUM2)

        new_tab()
        top_sites_section_2_rows_exists = exists(top_sites_section_2_rows, FirefoxSettings.FIREFOX_TIMEOUT)
        assert top_sites_section_2_rows_exists, 'In new tab, 16 cells are not displayed in a two rows'

        self.resize_browser('1000', '700')
        top_sites_section_resized_browser_2_rows_exists = exists(top_sites_section_resized_browser_2_rows,
                                                                 FirefoxSettings.FIREFOX_TIMEOUT)
        assert top_sites_section_resized_browser_2_rows_exists, 'After resizing, 12 cells are not displayed in two rows'

        self.top_site_dropdown(home_section_top_sites_most_visit_2_row, test_search_region, Key.NUM3)

        new_tab()
        top_sites_section_3_rows_exists = exists(top_sites_section_3_rows, FirefoxSettings.FIREFOX_TIMEOUT)
        assert top_sites_section_3_rows_exists, 'In new tab, 24 cells are not displayed in a three rows'

        self.resize_browser('1000', '700')
        top_sites_section_resized_browser_3_rows_exists = exists(top_sites_section_resized_browser_3_rows,
                                                                 FirefoxSettings.FIREFOX_TIMEOUT)
        assert top_sites_section_resized_browser_3_rows_exists, 'After resizing, 18 cells are not displayed in three ' \
                                                                'rows'
        self.top_site_dropdown(home_section_top_sites_most_visit_3_row, test_search_region, Key.NUM4)

        new_tab()
        hover(optional_footer_message_from_firefox)
        click(cross_mark_on_footer_message)
        wait(top_sites_section_4_rows)

        top_sites_section_4_rows_exists = exists(top_sites_section_4_rows, FirefoxSettings.FIREFOX_TIMEOUT)
        assert top_sites_section_4_rows_exists, 'In new tab, 32 cells are not displayed in a four rows'

        self.resize_browser('1000', '700')
        click(scroll_down_icon)
        top_sites_section_resized_browser_4_rows_exists = exists(top_sites_section_resized_browser_4_rows,
                                                                 FirefoxSettings.FIREFOX_TIMEOUT)
        assert top_sites_section_resized_browser_4_rows_exists, 'After resizing, 24 cells are not displayed in four ' \
                                                                'rows '

    def top_site_dropdown(self, dropdown_image: Pattern, test_region: Pattern, key_val):
        """Locate 'Top Sites' drop-down and change dropdown .
        :param dropdown_image: image Pattern.
        :param test_region: image Pattern, locator for sub-region of top site drop-down .
        :param key_val: Numeric key value from class Key(Enum).
        :return: None.
        """
        maximize_window()
        navigate('about:preferences#home')
        time.sleep(Settings.DEFAULT_UI_DELAY_SHORT)
        click(dropdown_image, None, region=test_region)
        type(key_val)
        type(Key.ENTER)

    def resize_browser(self, width, height):
        """resize browser to a specific width and height
        :param width: String (a number passed as string), Sets the width of the window, in pixels.
        :param height: String (a number passed as string), Sets the height of the window, in pixels.
        :return: None.
        """
        browser_console_opened_pattern = Pattern('browser_console_opened.png')
        clear_console_data = Pattern('clear_console_data.png')

        open_browser_console()
        try:
            wait(browser_console_opened_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        except FindError:
            raise FindError('The Browser Console couldn\'t open.')
        click(clear_console_data)
        click(browser_console_opened_pattern)
        paste('window.resizeTo(' + width + ',' + height + ')')
        type(Key.ENTER)
        time.sleep(Settings.DEFAULT_UI_DELAY_SHORT)
