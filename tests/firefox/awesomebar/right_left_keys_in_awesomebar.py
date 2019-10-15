# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="This test case navigates through the awesomebar suggestions/one-offs/settings gear using the "
        "right/left keys",
        locale=["en-US"],
        test_case_id="108277",
        test_suite_id="1902",
    )
    def run(self, firefox):
        search_with_google_one_off_string_pattern = Pattern(
            "google_one_off_highlighted.png"
        )
        settings_gear_highlighted_pattern = Pattern(
            "settings_gear_highlighted.png"
        ).similar(0.9)

        select_location_bar()
        paste("moz")

        assert scroll_until_pattern_found(
            search_with_google_one_off_string_pattern, type, (Key.DOWN,), 20, 1
        ), "The 'Google' button is highlighted when hitting the DOWN button."

        assert scroll_until_pattern_found(
            settings_gear_highlighted_pattern, type, (Key.DOWN,), 20, 1
        ), "The 'Google' button is highlighted when hitting the DOWN button."

        type(Key.RIGHT)

        one_off_first_highlighted = exists(
            search_with_google_one_off_string_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert one_off_first_highlighted, "The first one-off bar is selected again"

        assert scroll_until_pattern_found(
            settings_gear_highlighted_pattern, type, (Key.RIGHT,), 20, 1
        ), "The 'Google' button is highlighted when hitting the RIGHT button.."

        assert scroll_until_pattern_found(
            search_with_google_one_off_string_pattern, type, (Key.RIGHT,), 20, 1
        ), "The 'Google' button is highlighted when hitting the RIGHT button."

        assert scroll_until_pattern_found(
            settings_gear_highlighted_pattern, type, (Key.LEFT,), 20, 1
        ), "The 'Google' button is highlighted when hitting the LEFT button.."

        assert scroll_until_pattern_found(
            search_with_google_one_off_string_pattern.similar(0.9),
            type,
            (Key.LEFT,),
            20,
            1,
        ), "The 'Google' button is highlighted when hitting the LEFT button."
