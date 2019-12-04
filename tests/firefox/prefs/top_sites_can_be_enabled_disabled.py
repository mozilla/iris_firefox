# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Firefox can be set to display the home page on launch",
        locale=["en-US"],
        test_case_id="161666",
        test_suite_id="2241",
        blocked_by={"id": "4283", "platform": OSPlatform.MAC}
    )
    def run(self, firefox):
        top_sites_option_pattern = Pattern("top_sites_option.png")
        top_sites_reddit_pattern = Pattern("top_sites_reddit.png").similar(0.7)
        top_sites_amazon_pattern = Pattern("top_sites_amazon.png")
        top_sites_twitter_pattern = Pattern("top_sites_twitter.png")
        top_sites_facebook_pattern = Pattern("top_sites_facebook.png")
        top_sites_wikipedia_pattern = Pattern("top_sites_wikipedia.png")
        top_sites_youtube_pattern = Pattern("top_sites_youtube.png")

        navigate("about:preferences#home")

        preferences_page_opened = exists(top_sites_option_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert preferences_page_opened, "The about:preferences page is successfully loaded."

        top_sites = [
            top_sites_reddit_pattern,
            top_sites_amazon_pattern,
            top_sites_twitter_pattern,
            top_sites_facebook_pattern,
            top_sites_wikipedia_pattern,
            top_sites_youtube_pattern,
        ]

        top_sites_option_location = find(top_sites_option_pattern)
        top_sites_option_width, top_sites_option_height = top_sites_option_pattern.get_size()
        top_sites_option_region = Region(
            top_sites_option_location.x - top_sites_option_width,
            top_sites_option_location.y,
            top_sites_option_width * 2,
            top_sites_option_height,
        )

        top_sites_selected = exists(
            AboutPreferences.CHECKED_BOX, FirefoxSettings.FIREFOX_TIMEOUT, top_sites_option_region
        )
        assert top_sites_selected, "The option is selected by default."

        navigate("about:home")

        top_sites_displayed = exists(Utils.TOP_SITES, FirefoxSettings.FIREFOX_TIMEOUT)
        assert top_sites_displayed is True, "The Top Sites section is displayed"

        for site in top_sites:
            top_sites_listed = exists(site)
            assert top_sites_listed, "The site is listed by default"

        navigate("about:newtab")

        for site in top_sites:
            top_sites_listed = exists(site)
            assert top_sites_listed, "The site is listed by default"

        top_sites_displayed = exists(Utils.TOP_SITES, FirefoxSettings.FIREFOX_TIMEOUT)
        assert top_sites_displayed is True, "The Top Sites section is displayed in the New Tab"

        navigate("about:preferences#home")

        preferences_page_opened = exists(top_sites_option_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert preferences_page_opened, "The about:preferences page is successfully loaded."

        top_sites_selected = exists(
            AboutPreferences.CHECKED_BOX, FirefoxSettings.FIREFOX_TIMEOUT, top_sites_option_region
        )
        assert top_sites_selected, "The option is selected by default."

        top_sites_option_location = find(top_sites_option_pattern)
        top_sites_option_width, top_sites_option_height = top_sites_option_pattern.get_size()
        top_sites_option_region = Region(
            top_sites_option_location.x - top_sites_option_width,
            top_sites_option_location.y,
            top_sites_option_width * 2,
            top_sites_option_height,
        )

        click(AboutPreferences.CHECKED_BOX, region=top_sites_option_region)

        top_sites_selected = exists(
            AboutPreferences.UNCHECKED_BOX, FirefoxSettings.FIREFOX_TIMEOUT, top_sites_option_region
        )

        assert top_sites_selected, "The options is not selected anymore."

        navigate("about:home")

        google_logo_content_search_field = exists(Utils.TOP_SITES)
        assert google_logo_content_search_field is False, "The Top Sites section is not displayed on the Home Page"

        navigate("about:newtab")

        google_logo_content_search_field = exists(Utils.TOP_SITES)
        assert google_logo_content_search_field is False, "The Top Sites section is not displayed in the New Tab"

        new_window()

        time.sleep(Settings.DEFAULT_UI_DELAY)

        google_logo_content_search_field = exists(Utils.TOP_SITES)
        assert google_logo_content_search_field is False, "The Top Sites section is displayed in the New Window"
