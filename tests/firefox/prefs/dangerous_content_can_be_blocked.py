# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Dangerous and deceptive content can be blocked/unblocked",
        test_case_id="159261",
        test_suite_id="2241",
        locale=["en-US"],
    )
    def run(self, firefox):
        browser_privacy_hover_pattern = Pattern("browser_privacy_hover.png")
        desktop_download_warning_title_pattern = Pattern(
            "desktop_download_warning_title.png"
        )
        phishing_warning_label_pattern = Pattern("phishing_warning_label.png")
        link_label_pattern = Pattern("link_label.png")
        see_details_button_pattern = Pattern("see_details_button.png")
        block_dangerous_content_pattern = Pattern(
            "block_dangerous_deceptive_content.png"
        )
        phishing_page_loaded_pattern = Pattern("phishing_page_loaded.png")

        navigate("about:preferences#privacy")

        browser_privacy_label_exists = exists(
            browser_privacy_hover_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert browser_privacy_label_exists, "Privacy page is loaded"

        paste("software")

        block_dangerous_content_checked = exists(
            block_dangerous_content_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert block_dangerous_content_checked, (
            'The option is selected by default together with the "Block '
            'dangerous downloads" and "Warn you about unwanted and uncommon '
            'software" options. '
        )

        new_tab()
        navigate("https://testsafebrowsing.appspot.com/")

        test_page_opened = exists(
            desktop_download_warning_title_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT
        )
        assert test_page_opened, "The 'testsafebrowsing' page is properly loaded"

        width, height = phishing_warning_label_pattern.get_size()
        region = Rectangle(
            image_find(phishing_warning_label_pattern).x,
            image_find(phishing_warning_label_pattern).y,
            width,
            height,
        )
        click(link_label_pattern, region=region)

        see_details_button_displayed = exists(
            see_details_button_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
        )
        assert (
            see_details_button_displayed
        ), "A page warning you that the content is dangerous is displayed."

        previous_tab()

        click(block_dangerous_content_pattern)

        unchecked_box = exists(AboutPreferences.UNCHECKED_BOX)
        assert unchecked_box, "The option is not selected anymore."

        next_tab()
        click(NavBar.RELOAD_BUTTON)

        phishing_page_loaded = exists(
            phishing_page_loaded_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        see_details_button_not_displayed = not exists(
            see_details_button_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
        )
        assert phishing_page_loaded and see_details_button_not_displayed, (
            "The page is loaded without any warnings " "displayed. "
        )
