# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Firefox Home Content - Highlights can be displayed in 1 or 2 rows",
        locale=["en-US"],
        test_case_id="171440",
        test_suite_id="2241",
        preferences={'devtools.chrome.enabled': True}
    )
    def run(self, firefox):
        about_preferences_home_url_pattern = Pattern('about_preferences_home_url.png')
        home_page_highlights_pattern = Pattern('home_page_highlights.png').similar(0.7)
        highlights_no_of_row_drop_down_1_row = Pattern('home_top_sites_most_visit_default_value.png')
        top_site_option = Pattern('top_sites_option.png')
        web_search_options = Pattern('web_search_options.png')
        highlights_bookmark_soap = Pattern('highlights_bookmark_soap_test_site.png')
        highlights_bookmark_firefox = Pattern('highlights_bookmark_firefox_test_site.png')
        highlights_bookmark_focus = Pattern('highlights_bookmark_focus_test_site.png')
        highlights_bookmark_mozilla_1 = Pattern('highlights_bookmark_mozilla_test_site_1.png').similar(0.7)
        highlights_bookmark_download = Pattern('highlights_bookmark_download_test_site.png')
        highlights_bookmark_pocket_1 = Pattern('highlights_bookmark_pocket_test_site_1.png')
        highlights_bookmark_mozilla_2 = Pattern('highlights_bookmark_mozilla_test_site_2.png')
        highlights_bookmark_pocket_2 = Pattern('highlights_bookmark_pocket_test_site_2.png')
        cross_mark_on_footer_message = Pattern('cross_mark_on_footer_message.png')
        optional_footer_message_from_firefox = Pattern('optional_footer_message_from_firefox.png')

        if OSHelper.is_linux():
            highlights_options_pattern = Pattern("highlights_search_result.png")
        else:
            highlights_options_pattern = Pattern("highlights_option.png")

        bookmark_sites_url = [
            LocalWeb.POCKET_TEST_SITE_2,
            LocalWeb.MOZILLA_TEST_SITE_2,
            LocalWeb.POCKET_TEST_SITE,
            LocalWeb.DOWNLOAD_TEST_SITE,
            LocalWeb.MOZILLA_TEST_SITE,
            LocalWeb.FOCUS_TEST_SITE,
            LocalWeb.FIREFOX_TEST_SITE,
            LocalWeb.SOAP_WIKI_TEST_SITE,
        ]
        # Create bookmarks
        for site in bookmark_sites_url:
            bookmark_button_pattern = LocationBar.STAR_BUTTON_UNSTARRED
            navigate(site)
            bookmark_button_pattern_exists = exists(bookmark_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            assert bookmark_button_pattern_exists, "Bookmark star is not present on the page"
            click(bookmark_button_pattern)
            page_bookmarked_assert = exists(Bookmarks.StarDialog.NEW_BOOKMARK, FirefoxSettings.FIREFOX_TIMEOUT)
            assert page_bookmarked_assert, "The page couldn't bookmarked via the star button."

        new_tab()
        navigate("about:preferences#home")
        about_preferences_home_url_exists = exists(about_preferences_home_url_pattern,
                                                   FirefoxSettings.FIREFOX_TIMEOUT)
        assert about_preferences_home_url_exists, \
            'Home section of about:preferences page could not be loaded successfully'

        click(AboutPreferences.FIND_IN_OPTIONS)
        paste('Highlights')
        click(top_site_option)
        click(web_search_options)

        preferences_page_opened = exists(highlights_options_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert preferences_page_opened, "Highlights section is not present in the about:preferences page."

        highlights_option_location = find(highlights_options_pattern)
        highlights_option_width, highlights_option_height = (
            highlights_options_pattern.get_size()
        )
        highlights_option_region = Region(
            highlights_option_location.x - highlights_option_width,
            highlights_option_location.y - highlights_option_height / 2,
            highlights_option_width * 2,
            highlights_option_height * 2,
        )

        highlights_option_selected = exists(
            AboutPreferences.CHECKED_BOX,
            FirefoxSettings.FIREFOX_TIMEOUT,
            highlights_option_region,
        )
        assert highlights_option_selected, "Checkbox option present in 'Highlights' is not selected by default"

        highlights_option_drop_down_region = Region(
            highlights_option_location.x,
            highlights_option_location.y - highlights_option_height / 2,
            highlights_option_width * 7,
            highlights_option_height * 4,
        )
        highlights_option_default_drop_down_value = exists(
            highlights_no_of_row_drop_down_1_row,
            FirefoxSettings.FIREFOX_TIMEOUT,
            highlights_option_drop_down_region,
        )
        assert highlights_option_default_drop_down_value, \
            "Highlights option default drop down value is not 1 row"

        navigate("about:home")
        home_page_highlights_pattern_found = exists(home_page_highlights_pattern,
                                                    FirefoxSettings.FIREFOX_TIMEOUT)
        assert home_page_highlights_pattern_found, "The Highlights section is not displayed on the Homepage."
        navigate("about:newtab")
        home_page_highlights_pattern_found = exists(home_page_highlights_pattern,
                                                    FirefoxSettings.FIREFOX_TIMEOUT)
        assert home_page_highlights_pattern_found, "The Highlights section is not displayed on the Homepage."
        highlights_region_1_row_4_cells = self.region_creation_highlights(highlights_bookmark_soap, 2, 3.25, 5.5, 4.5)
        bookmark_sites_default_view_1_row = [
            highlights_bookmark_soap,
            highlights_bookmark_focus,
            highlights_bookmark_firefox,
            highlights_bookmark_mozilla_1
        ]
        for site in bookmark_sites_default_view_1_row:
            site_displayed_in_highlights = exists(site, FirefoxSettings.FIREFOX_TIMEOUT,
                                                  region=highlights_region_1_row_4_cells)
            assert site_displayed_in_highlights, \
                "{} image is not displayed in default highlight view when number of row is 1 with 4 cells".format(site)

        bookmark_sites_highlights_reduced_view_3_cells = [
            highlights_bookmark_soap,
            highlights_bookmark_focus,
            highlights_bookmark_firefox
        ]
        self.resize_browser('1000', '700')

        highlights_region_1_row_3_cells = self.region_creation_highlights(highlights_bookmark_soap, 2, 3.25, 4.125,
                                                                          4.5)
        for site in bookmark_sites_highlights_reduced_view_3_cells:
            site_displayed_in_highlights = exists(site, FirefoxSettings.FIREFOX_TIMEOUT,
                                                  region=highlights_region_1_row_3_cells)
            assert site_displayed_in_highlights, \
                "{} image is not displayed in resized highlight view when number of row is 1 with 3 cells".format(site)

        self.resize_browser('750', '800')

        highlights_region_2_rows_3_cells = self.region_creation_highlights(highlights_bookmark_soap, 2, 3.25, 2.75,
                                                                           9)
        for site in bookmark_sites_highlights_reduced_view_3_cells:
            site_displayed_in_highlights = exists(site, FirefoxSettings.FIREFOX_TIMEOUT,
                                                  region=highlights_region_2_rows_3_cells)
            assert site_displayed_in_highlights, \
                "{} image is not displayed in resized highlight view " \
                "when number of rows are 2 with 3 cells".format(site)

        self.highlights_option_drop_down(highlights_no_of_row_drop_down_1_row,
                                         highlights_option_drop_down_region)
        previous_tab()

        bookmark_sites_modified_view_8_cells = [
            highlights_bookmark_soap,
            highlights_bookmark_focus,
            highlights_bookmark_firefox,
            highlights_bookmark_mozilla_1,
            highlights_bookmark_download,
            highlights_bookmark_pocket_1,
            highlights_bookmark_mozilla_2,
            highlights_bookmark_pocket_2
        ]

        highlights_region_2_rows_8_cells = self.region_creation_highlights(highlights_bookmark_soap, 2, 3.25, 5.5,
                                                                           9)
        for site in bookmark_sites_modified_view_8_cells:
            site_displayed_in_highlights = exists(site, FirefoxSettings.FIREFOX_TIMEOUT,
                                                  region=highlights_region_2_rows_8_cells)
            assert site_displayed_in_highlights, \
                "{} image is not displayed in modified highlight view " \
                "when number of rows are 2 with 8 cells".format(site)

        bookmark_sites_modified_view_6_cells = [
            highlights_bookmark_soap,
            highlights_bookmark_focus,
            highlights_bookmark_firefox,
            highlights_bookmark_mozilla_1,
            highlights_bookmark_download,
            highlights_bookmark_pocket_1
        ]
        self.resize_browser('1000', '700')
        highlights_region_2_rows_6_cells = self.region_creation_highlights(highlights_bookmark_soap, 2, 3.25, 4.125,
                                                                           9)
        for site in bookmark_sites_modified_view_6_cells:
            site_displayed_in_highlights = exists(site, FirefoxSettings.FIREFOX_TIMEOUT,
                                                  region=highlights_region_2_rows_6_cells)
            assert site_displayed_in_highlights, \
                "{} image is not displayed in modified highlight view " \
                "when number of rows are 2 with 6 cells".format(site)

        self.resize_browser('750', '800')
        optional_footer_message_from_firefox_exists = exists(optional_footer_message_from_firefox)
        if optional_footer_message_from_firefox_exists:
            hover(optional_footer_message_from_firefox)
            footer_message_location = find(optional_footer_message_from_firefox)
            footer_message_region = Region(
                footer_message_location.x,
                footer_message_location.y,
                Screen.SCREEN_WIDTH,
                Screen.SCREEN_HEIGHT // 5,
            )
            cross_mark_on_footer_message_exists = exists(cross_mark_on_footer_message,
                                                         FirefoxSettings.FIREFOX_TIMEOUT, region=footer_message_region)
            if cross_mark_on_footer_message_exists:
                click(cross_mark_on_footer_message, region=footer_message_region)
                click(cross_mark_on_footer_message, region=footer_message_region)
        type(Key.DOWN)
        type(Key.DOWN)
        highlights_region_3_rows_6_cells = self.region_creation_highlights(highlights_bookmark_soap, 2, 1, 3.25, 13)
        for site in bookmark_sites_modified_view_6_cells:
            site_displayed_in_highlights = exists(site, FirefoxSettings.FIREFOX_TIMEOUT,
                                                  region=highlights_region_3_rows_6_cells)
            assert site_displayed_in_highlights, \
                "{} image is not displayed in modified highlight view " \
                "when number of rows are 3 with 6 cells".format(site)

    @staticmethod
    def highlights_option_drop_down(drop_down_image: Pattern, test_region: Pattern):
        """Locate 'Highlights' option drop-down and increase it's value by 1 with respect to 'param' drop_down_image.
        :param drop_down_image: image Pattern.
        :param test_region: image Pattern, locator for sub-region of highlights section drop down .
        :return: None.
        """
        if OSHelper.is_linux():
            click(MainWindow.MAXIMIZE_BUTTON)
        else:
            maximize_window()
        previous_tab()
        navigate("about:preferences#home")
        click(AboutPreferences.FIND_IN_OPTIONS)
        paste('Highlights')
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
        browser_console_opened_pattern = Pattern('browser_console_opened.png')
        clear_console_data = Pattern('clear_console_data.png')
        open_browser_console()
        try:
            wait(browser_console_opened_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        except FindError:
            raise FindError("The Browser Console couldn't open.")
        click(clear_console_data)
        click(browser_console_opened_pattern)
        paste('window.resizeTo(' + width + ',' + height + ')')
        type(Key.ENTER)
        time.sleep(Settings.DEFAULT_UI_DELAY_SHORT)
        if OSHelper.is_linux():
            type(text=Key.F4, modifier=KeyModifier.ALT)
        click(Pattern('new_tab_icon.png'))
        time.sleep(Settings.DEFAULT_MOVE_MOUSE_DELAY)

    @staticmethod
    def region_creation_highlights(first_highlights_cell_image, x, y, width, height):
        """Create region to validate if cells are in specific row/column or not
        :param first_highlights_cell_image: image Pattern, Image pattern for First highlight cell
        :param x: Integer Number, Value to change 'x' Coordinate position of first_highlights_cell_image
        :param y: floating point number, Value to change 'y' Coordinate position of first_highlights_cell_image
        :param width: floating point number,  Value to increase width of the region, in pixels.
        :param height: floating point number, Value to increase height of the region, in pixels.
        :return: None.
        """
        highlights_option_1st_cell_location = find(first_highlights_cell_image)
        highlights_cell_width, highlights_cell_height = first_highlights_cell_image.get_size()
        highlights_region = Region(
            highlights_option_1st_cell_location.x - highlights_cell_width / x,
            highlights_option_1st_cell_location.y - highlights_cell_height * y,
            highlights_cell_width * width,
            highlights_cell_height * height,
        )
        return highlights_region
