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
        home_page_highlights_pattern = Pattern('home_page_highlights.png').similar(0.6)
        highlights_no_of_row_drop_down_1_row = Pattern('home_top_sites_most_visit_default_value.png')
        top_site_option = Pattern('top_sites_option.png')
        web_search_options = Pattern('web_search_options.png')
        highlights_bookmark_facebook = Pattern('highlights_bookmark_facebook.png')
        highlights_bookmark_github = Pattern('highlights_bookmark_github.png')
        highlights_bookmark_mozilla = Pattern('highlights_bookmark_mozilla.png')
        highlights_bookmark_google = Pattern('highlights_bookmark_google.png')
        highlights_bookmark_firefox = Pattern('highlights_bookmark_firefox.png')
        highlights_bookmark_amazon = Pattern('highlights_bookmark_amazon.png')
        highlights_bookmark_outlook = Pattern('highlights_bookmark_outlook.png')
        highlights_bookmark_youtube = Pattern('highlights_bookmark_youtube.png')
        if OSHelper.is_linux():
            highlights_options_pattern = Pattern("highlights_search_result.png")
        else:
            highlights_options_pattern = Pattern("highlights_option.png")

        bookmark_sites_url = [
            'https://www.amazon.com/',
            'https://outlook.live.com/owa/',
            'https://www.youtube.com/',
            'https://www.mozilla.org/en-US/firefox/new/',
            'https://www.google.com/',
            'https://github.com/',
            'https://www.mozilla.org/en-US/',
            'https://www.facebook.com/',
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

        bookmark_sites_default_view_1_row = [
            highlights_bookmark_facebook,
            highlights_bookmark_mozilla,
            highlights_bookmark_github,
            highlights_bookmark_google
        ]
        for site in bookmark_sites_default_view_1_row:
            top_sites_listed = exists(site)
            assert top_sites_listed, "For default view, 4 highlight cells are not displayed in new_tab/home page"

        # Resize browser - 3 highlights cell in a row
        bookmark_sites_highlights_reduced_view_3_cells = [
            highlights_bookmark_facebook,
            highlights_bookmark_mozilla,
            highlights_bookmark_github
        ]
        self.resize_browser('1000', '700')
        for site in bookmark_sites_highlights_reduced_view_3_cells:
            top_sites_listed = exists(site)
            assert top_sites_listed, "For reduced default view, " \
                                     "3 highlight cells are not displayed in 1 row"

        # Resize browser - 3 highlights cell in two rows
        self.resize_browser('750', '700')
        for site in bookmark_sites_highlights_reduced_view_3_cells:
            top_sites_listed = exists(site)
            assert top_sites_listed, "For further reduced default view, " \
                                     "3 highlight cells are not displayed in 2 row"

        self.highlights_option_drop_down(highlights_no_of_row_drop_down_1_row,
                                         highlights_option_drop_down_region)
        previous_tab()

        # 8 highlight cells in two rows
        bookmark_sites_modified_view_8_cells = [
            highlights_bookmark_facebook,
            highlights_bookmark_mozilla,
            highlights_bookmark_github,
            highlights_bookmark_google,
            highlights_bookmark_firefox,
            highlights_bookmark_amazon,
            highlights_bookmark_outlook,
            highlights_bookmark_youtube
        ]
        for site in bookmark_sites_modified_view_8_cells:
            top_sites_listed = exists(site)
            assert top_sites_listed, "For 2 highlights rows, 8 cells are not displayed in new_tab/home page"

        # Resize browser - 6 highlights cell in 2 rows
        bookmark_sites_modified_view_6_cells = [
            highlights_bookmark_facebook,
            highlights_bookmark_mozilla,
            highlights_bookmark_github,
            highlights_bookmark_google,
            highlights_bookmark_firefox,
            highlights_bookmark_youtube
        ]
        self.resize_browser('1000', '700')
        for site in bookmark_sites_modified_view_6_cells:
            top_sites_listed = exists(site)
            assert top_sites_listed, "For reduced modified view, " \
                                     "6 highlight cells are not displayed in 2 rows"

        # Resize browser - 6 highlights cells in 3 rows
        self.resize_browser('750', '700')
        type(Key.PAGE_DOWN)
        for site in bookmark_sites_modified_view_6_cells:
            top_sites_listed = exists(site)
            assert top_sites_listed, "For further reduced modified view, " \
                                     "6 highlight cells are not displayed in 3 rows"

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
        click(Pattern('new_tab_icon.png'))
