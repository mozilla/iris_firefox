# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Firefox Home Content - Recommended by Pocket",
        locale=["en-US"],
        test_case_id="161668",
        test_suite_id="2241",
    )
    def run(self, firefox):
        recommended_by_pocket_option = Pattern("recommended_by_pocket_option.png")
        recommended_by_pocket_label_pattern = Pattern(
            "recommended_by_pocket_label.png"
        ).similar(0.7)

        change_preference(
            "browser.newtabpage.activity-stream.feeds.section.topstories", "true"
        )
        change_preference("browser.search.region", "US")

        firefox.restart(
            url="about:preferences#home", image=recommended_by_pocket_option
        )

        navigate("about:preferences#home")

        preferences_page_opened = exists(
            recommended_by_pocket_option, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert preferences_page_opened, (
            'The option "Recommended by Pocket" is displayed and has the '
            "corresponding icon "
        )

        pocket_option_location = find(recommended_by_pocket_option)
        width, height = recommended_by_pocket_option.get_size()
        pocket_option_region = Region(
            pocket_option_location.x - width,
            pocket_option_location.y,
            width * 2,
            height,
        )

        pocket_option_selected = exists(
            AboutPreferences.CHECKED_BOX, region=pocket_option_region
        )
        assert pocket_option_selected, "The option is selected by default."

        navigate("about:home")

        pocket_section_displayed = exists(
            recommended_by_pocket_label_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            pocket_section_displayed
        ), "The Recommended by Pocket section is displayed underneath Top Sites section."

        new_tab()

        pocket_section_displayed = exists(
            recommended_by_pocket_label_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            pocket_section_displayed
        ), "The Recommended by Pocket section is displayed underneath Top Sites section."

        navigate("about:preferences#home")

        preferences_page_opened = exists(
            recommended_by_pocket_option, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert preferences_page_opened, (
            'The option "Recommended by Pocket" is displayed and has the '
            "corresponding icon "
        )

        pocket_option_location = find(recommended_by_pocket_option)
        width, height = recommended_by_pocket_option.get_size()
        pocket_option_region = Region(
            pocket_option_location.x - width,
            pocket_option_location.y,
            width * 2,
            height,
        )

        pocket_option_selected = exists(
            AboutPreferences.CHECKED_BOX, region=pocket_option_region
        )
        assert pocket_option_selected, "The option is selected by default."

        click(AboutPreferences.CHECKED_BOX, region=pocket_option_region)

        pocket_option_selected = exists(
            AboutPreferences.UNCHECKED_BOX, region=pocket_option_region
        )
        assert pocket_option_selected, "The option is not selected anymore."

        navigate("about:home")

        pocket_section_displayed = not exists(recommended_by_pocket_label_pattern)
        assert (
            pocket_section_displayed
        ), "The Recommended by Pocket section is not displayed anymore"

        new_tab()

        pocket_section_displayed = not exists(recommended_by_pocket_label_pattern)
        assert (
            pocket_section_displayed
        ), "The Recommended by Pocket section is not displayed anymore"

        new_window()

        pocket_section_displayed = not exists(recommended_by_pocket_label_pattern)
        assert (
            pocket_section_displayed
        ), "The Recommended by Pocket section is not displayed anymore"
