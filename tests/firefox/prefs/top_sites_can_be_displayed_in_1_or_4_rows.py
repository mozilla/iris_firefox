# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Firefox Home Content - Top Sites can be displayed in 1 or 4 rows",
        test_case_id="161667",
        test_suite_id="2241",
        locale=["en-US"],
        preferences={"devtools.chrome.enabled": True},
    )
    def run(self, firefox):
        top_sites_drop_down_1_row_pattern = Pattern("home_top_sites_most_visit_default_value.png")
        top_sites_drop_down_2_row_pattern = Pattern("home_top_sites_most_visit_2_row.png")
        top_sites_drop_down_3_row_pattern = Pattern("home_top_sites_most_visit_3_row.png")
        top_sites_option_pattern = Pattern("top_sites_option.png")
        top_sites_reddit_pattern = Pattern("top_sites_reddit.png")
        top_sites_amazon_pattern = Pattern("top_sites_amazon.png")
        top_sites_twitter_pattern = Pattern("top_sites_twitter.png")
        top_sites_facebook_pattern = Pattern("top_sites_facebook.png")
        top_sites_wikipedia_pattern = Pattern("top_sites_wikipedia.png")
        top_sites_youtube_pattern = Pattern("top_sites_youtube.png")
        top_sites_empty_box_pattern = Pattern("top_sites_empty_box_pattern.png")
        web_search_options = Pattern('web_search_options.png')

        navigate("about:preferences#home")
        preferences_page_opened = exists(top_sites_option_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert preferences_page_opened, "about:preferences#home page could not loaded successfully"
        click(web_search_options)

        top_sites_option_location = find(top_sites_option_pattern)
        top_sites_option_width, top_sites_option_height = top_sites_option_pattern.get_size()

        # Small top site region to verify checkbox status in about:preferences
        top_sites_option_region = Region(
            top_sites_option_location.x - top_sites_option_width,
            top_sites_option_location.y,
            top_sites_option_width * 2,
            top_sites_option_height,
        )

        top_sites_selected = exists(
            AboutPreferences.CHECKED_BOX, FirefoxSettings.FIREFOX_TIMEOUT, top_sites_option_region
        )
        assert top_sites_selected, "The option 'Top Sites' is not selected by default."

        # Full top site region in about:preferences to verify top site row selector drop-down
        full_top_site_region = Region(
            0,
            top_sites_option_location.y - top_sites_option_height / 2,
            Screen.SCREEN_WIDTH,
            top_sites_option_height * 3
        )
        top_sites_drop_down_1_row_pattern_found = exists(top_sites_drop_down_1_row_pattern,
                                                         FirefoxSettings.FIREFOX_TIMEOUT,
                                                         region=full_top_site_region,
                                                         )
        assert top_sites_drop_down_1_row_pattern_found, 'Default number of rows for "Top Sites" is not selected as 1'

        default_top_sites_list = [
            top_sites_reddit_pattern,
            top_sites_amazon_pattern,
            top_sites_twitter_pattern,
            top_sites_facebook_pattern,
            top_sites_wikipedia_pattern,
            top_sites_youtube_pattern,
        ]

        new_tab()
        home_and_new_tab_list = ["about:home", "about:newtab"]
        for navigation_page in home_and_new_tab_list:
            navigate(navigation_page)
            top_sites_displayed = exists(Utils.TOP_SITES, FirefoxSettings.FIREFOX_TIMEOUT)
            assert top_sites_displayed, "The Top Sites section is not displayed in {} page".format(navigation_page)

        new_private_window()
        top_sites_displayed = exists(Utils.TOP_SITES, FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        assert top_sites_displayed is False, "The Top Sites section is displaying in the private window"
        close_tab()

        # Validate 8 sites in 1 row
        eight_sites_in_one_row = default_top_sites_list.copy()
        for _ in range(2):
            eight_sites_in_one_row.append(top_sites_empty_box_pattern)
        self.sites_displayed_in_top_sites_section(1, 8, eight_sites_in_one_row)

        # Validate 6 sites in 1 row : after resizing
        self.resize_browser("1000", "700")
        self.sites_displayed_in_top_sites_section(1, 6, default_top_sites_list)

        self.top_site_drop_down(top_sites_drop_down_1_row_pattern, full_top_site_region)
        previous_tab()

        # Validate 16 sites in 2 rows
        sixteen_sites_in_two_rows = default_top_sites_list.copy()
        for _ in range(10):
            sixteen_sites_in_two_rows.append(top_sites_empty_box_pattern)
        self.sites_displayed_in_top_sites_section(2, 16, sixteen_sites_in_two_rows)

        # Validate 12 sites in 2 rows : after resizing
        self.resize_browser("1000", "700")
        twelve_sites_in_two_rows = default_top_sites_list.copy()
        for _ in range(6):
            twelve_sites_in_two_rows.append(top_sites_empty_box_pattern)
        self.sites_displayed_in_top_sites_section(2, 12, twelve_sites_in_two_rows)

        self.top_site_drop_down(top_sites_drop_down_2_row_pattern, full_top_site_region)
        previous_tab()

        # Validate 24 sites in 3 rows
        twenty_four_sites_in_three_rows = default_top_sites_list.copy()
        for _ in range(18):
            twenty_four_sites_in_three_rows.append(top_sites_empty_box_pattern)
        self.sites_displayed_in_top_sites_section(3, 24, twenty_four_sites_in_three_rows)

        # Validate 18 sites in 3 rows : after resizing
        self.resize_browser("1000", "700")
        eighteen_sites_in_three_rows = default_top_sites_list.copy()
        for _ in range(12):
            eighteen_sites_in_three_rows.append(top_sites_empty_box_pattern)
        self.sites_displayed_in_top_sites_section(3, 18, eighteen_sites_in_three_rows)

        self.top_site_drop_down(top_sites_drop_down_3_row_pattern, full_top_site_region)
        previous_tab()
        type(Key.DOWN)

        # Validate 32 sites in 4 rows
        thirty_two_sites_in_four_rows = default_top_sites_list.copy()
        for _ in range(26):
            thirty_two_sites_in_four_rows.append(top_sites_empty_box_pattern)
        self.sites_displayed_in_top_sites_section(4, 32, thirty_two_sites_in_four_rows)

        # Validate 24 sites in 4 rows : after resizing
        self.resize_browser("1000", "700")
        twenty_four_sites_in_four_rows = default_top_sites_list.copy()
        for _ in range(18):
            twenty_four_sites_in_four_rows.append(top_sites_empty_box_pattern)
        self.sites_displayed_in_top_sites_section(4, 24, twenty_four_sites_in_four_rows)

    @staticmethod
    def top_site_drop_down(drop_down_image: Pattern, test_region: Pattern):
        """Locate 'Top Sites' drop-down and change drop-down .
        :param drop_down_image: image Pattern.
        :param test_region: image Pattern, locator for sub-region of top site drop-down .
        :return: None.
        """
        if OSHelper.is_linux():
            click(MainWindow.MAXIMIZE_BUTTON)
        else:
            maximize_window()
        previous_tab()
        click(drop_down_image, None, region=test_region)
        type(Key.DOWN)
        time.sleep(Settings.DEFAULT_KEY_SHORTCUT_DELAY)
        type(Key.ENTER)

    @staticmethod
    def resize_browser(width, height):
        """resize browser to a specific width and height
        :param width: String (a number passed as string), Sets the width of the window, in pixels.
        :param height: String (a number passed as string), Sets the height of the window, in pixels.
        :return: None.
        """
        browser_console_opened_pattern = Pattern("browser_console_opened.png")
        clear_console_data = Pattern("clear_console_data.png")
        open_browser_console()
        try:
            wait(browser_console_opened_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        except FindError:
            raise FindError("The Browser Console couldn't open.")
        click(clear_console_data)
        click(browser_console_opened_pattern)
        paste("window.resizeTo(" + width + "," + height + ")")
        type(Key.ENTER)
        time.sleep(Settings.DEFAULT_UI_DELAY_SHORT)
        if OSHelper.is_linux():
            type(text=Key.F4, modifier=KeyModifier.ALT)
        click(Pattern('new_tab_icon.png'))
        time.sleep(Settings.DEFAULT_MOVE_MOUSE_DELAY)

    @staticmethod
    def sites_displayed_in_top_sites_section(no_of_rows, no_of_top_sites_boxes, top_site_list):
        """Create region to validate if cells are in specific row/column or not
        :param no_of_rows: Integer Number, Number of rows in top sites section
        :param no_of_top_sites_boxes: Integer Number, Top sites displayed in top sites section
        :param top_site_list: list,  List of all the sites displayed in top sites section.
        :return: None.
        """
        top_sites_first_box_pattern = Pattern("top_sites_first_box_pattern.png")

        top_sites_first_box_found = exists(top_sites_first_box_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert top_sites_first_box_found, "Top sites first box is not visible in current page"
        top_sites_first_box_location = find(top_sites_first_box_pattern)
        top_sites_cell_width, top_sites_cell_height = top_sites_first_box_pattern.get_size()
        top_sites_region = Region(
            top_sites_first_box_location.x,
            top_sites_first_box_location.y,
            top_sites_cell_width * no_of_top_sites_boxes / no_of_rows,
            top_sites_cell_height * no_of_rows,
        )
        for site in top_site_list:
            if top_site_list.index(site) < 6:
                top_site_full_path = format(site)
                site_name_with_bracket = re.split(".png", top_site_full_path)
                top_site_name = (str(site_name_with_bracket[0]).replace("(", " "))
                top_site_found = exists(site, FirefoxSettings.SHORT_FIREFOX_TIMEOUT, region=top_sites_region)
                assert top_site_found, \
                    "{} couldn't find listed by default in top site section.".format(top_site_name)
            else:
                top_site_found = exists(site, FirefoxSettings.SHORT_FIREFOX_TIMEOUT, region=top_sites_region)

                if no_of_top_sites_boxes in [8, 16, 24, 32]:
                    error_msg = "{} top sites are not present in {} row(s) in normal mode". \
                        format(no_of_top_sites_boxes, no_of_rows)
                elif no_of_top_sites_boxes in [6, 12, 18]:
                    error_msg = "{} top sites are not present in {} row(s) in resized mode". \
                        format(no_of_top_sites_boxes, no_of_rows)
                elif no_of_top_sites_boxes == 24:
                    if no_of_rows == 3:
                        error_msg = "{} top sites are not present in {} row(s) in normal mode". \
                            format(no_of_top_sites_boxes, no_of_rows)
                    elif no_of_rows == 4:
                        error_msg = "{} top sites are not present in {} row(s) in resized mode". \
                            format(no_of_top_sites_boxes, no_of_rows)
                else:
                    error_msg = "Wrong no_of_rows passed as an argument"

            assert top_site_found, error_msg
