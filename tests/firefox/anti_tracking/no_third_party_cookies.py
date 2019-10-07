# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Firefox can be set to no longer accept third-party cookies.",
        locale=["en-US"],
        test_case_id="106156",
        test_suite_id="1826",
    )
    def run(self, firefox):
        all_third_party_cookies_pattern = Pattern("all_third_party_cookies.png")
        cookies_list_empty_pattern = Pattern("cookies_list_empty.png")
        block_cookies_ticked_pattern = Pattern("block_cookies_ticked.png").similar(0.9)
        block_cookies_unticked_pattern = Pattern("block_cookies_unticked.png").similar(
            0.9
        )
        cookies_window_title_pattern = Pattern("cookies_window_title.png")
        custom_content_blocking_unticked_pattern = Pattern(
            "custom_content_blocking_unticked.png"
        )
        custom_content_blocking_ticked_pattern = Pattern(
            "custom_content_blocking_ticked.png"
        )
        manage_cookies_data_pattern = Pattern("manage_cookies_data.png")
        site_cookie_one_pattern = Pattern("site_cookie_one.png")
        site_cookie_two_pattern = Pattern("site_cookie_two.png")
        site_tab_pattern = Pattern("prosport_tab.png")

        if OSHelper.is_windows():
            value = 200
        else:
            value = 10

        navigate("about:preferences#privacy")

        Mouse().move(
            Location(Screen.SCREEN_WIDTH // 2, Screen.SCREEN_HEIGHT // 2),
            FirefoxSettings.TINY_FIREFOX_TIMEOUT,
        )

        preferences_opened = scroll_until_pattern_found(
            custom_content_blocking_unticked_pattern, Mouse().scroll, (0, -value), 100
        )
        assert (
            preferences_opened
        ), "The privacy preferences page is successfully displayed."

        click(custom_content_blocking_unticked_pattern)

        cookies_blocking_unticked = exists(block_cookies_unticked_pattern)

        if cookies_blocking_unticked:

            click(block_cookies_unticked_pattern, 1)

        cookies_blocking_ticked = exists(block_cookies_ticked_pattern.similar(0.6))
        assert cookies_blocking_ticked, "Ticked blocking cookies checkbox"

        block_cookies_location = find(block_cookies_ticked_pattern)

        option_width, option_height = block_cookies_ticked_pattern.get_size()
        block_cookies_option_list = Location(
            block_cookies_location.x + (option_width * 5), block_cookies_location.y
        )

        click(block_cookies_option_list)

        time.sleep(Settings.DEFAULT_UI_DELAY)

        repeat_key_down(2)

        type(Key.ENTER)

        all_third_party_cookies = exists(all_third_party_cookies_pattern)
        assert (
            all_third_party_cookies
        ), "All third-party cookies (may cause websites to break)"

        navigate("https://www.prosport.ro/")

        site_loaded = exists(site_tab_pattern, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT)
        assert site_loaded, 'The "Prosport" website is successfully displayed.'

        new_tab()

        navigate("about:preferences#privacy")

        preferences_opened = exists(custom_content_blocking_ticked_pattern)
        assert preferences_opened, "The page is successfully displayed."

        paste("manage data")

        cookies_data_button_located = exists(manage_cookies_data_pattern)
        assert cookies_data_button_located, '"Manage Data..." button displayed.'

        click(manage_cookies_data_pattern)

        cookies_data_window_opened = exists(cookies_window_title_pattern)
        assert cookies_data_window_opened, "Cookies data window opened."

        site_cookie_one_saved = exists(site_cookie_one_pattern)
        assert site_cookie_one_saved, "Target site cookie saved."

        click(site_cookie_one_pattern)
        type(Key.DELETE)

        site_cookie_two_saved = exists(site_cookie_two_pattern)
        assert site_cookie_two_saved, "Other target cookie saved."

        click(site_cookie_two_pattern)
        type(Key.DELETE)

        type(Key.DELETE)  # There are two default cookies from mozilla
        type(
            Key.DELETE
        )  # So it's needed to press "Delete" key twice to remove this site's cookies from list

        cookies_list_is_empty = exists(cookies_list_empty_pattern)
        assert cookies_list_is_empty, "No third-party cookies are saved"
