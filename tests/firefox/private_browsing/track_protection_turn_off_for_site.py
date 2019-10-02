# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Tracking Protection can be turned off for individual sites",
        test_case_id="107431",
        test_suite_id="1826",
        locales=["en-US"],
    )
    def run(self, firefox):
        tracking_protection_shield_pattern = Pattern(
            "tracking_protection_shield_activated.png"
        )
        tracking_protection_shield_deactivated_pattern = (
            LocationBar.TRACKING_PROTECTION_SHIELD_DEACTIVATED
        )
        cnn_site_logo_pattern = LocalWeb.CNN_LOGO
        cnn_blocked_content_pattern = LocalWeb.CNN_BLOCKED_CONTENT_ADV
        disable_blocking_button_pattern = Pattern(
            "turn_off_blocking_for_site_button.png"
        )
        enable_blocking_button_pattern = Pattern("turn_on_blocking_for_site_button.png")
        tracking_content_detected_message_pattern = Pattern(
            "tracking_protection_is_off.png"
        )
        tracking_attempts_blocked_message_pattern = Pattern(
            "tracking_protection_is_on.png"
        )
        trackers_popup_title_pattern = Pattern("trackers_popup_title.png")
        trackers_button_pattern = Pattern("open_trackers_list.png")
        blocked_tracker_label_pattern = Pattern("blocked_tracker_label.png")
        trackers_icon_pattern = Pattern("not_detected_trackers_list.png")

        restore_firefox_focus()

        new_private_window()

        private_browsing_window_loaded = exists(
            PrivateWindow.private_window_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            private_browsing_window_loaded
        ), "A new private window is successfully opened"

        navigate("https://edition.cnn.com/?refresh=1")

        website_displayed = exists(
            cnn_site_logo_pattern, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT + 100
        )
        assert website_displayed, "The website is successfully displayed"

        tracking_protection_shield_displayed = exists(
            tracking_protection_shield_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            tracking_protection_shield_displayed
        ), "The tracking protection shield is displayed"

        restore_firefox_focus()
        cnn_blocked_content_displayed = scroll_until_pattern_found(
            cnn_blocked_content_pattern,
            type,
            (Key.PAGE_DOWN,),
            10,
            timeout=FirefoxSettings.TINY_FIREFOX_TIMEOUT / 3,
        )
        assert cnn_blocked_content_displayed is False, (
            "Websites content that contain tracking"
            " elements are not displayed on the page"
        )
        page_home()

        click(tracking_protection_shield_pattern)

        disable_blocking_button_displayed = exists(
            disable_blocking_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            disable_blocking_button_displayed
        ), "The 'Site information' panel is displayed"

        trackers_button_available = exists(
            trackers_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert trackers_button_available, (
            "'Trackers' button is displayed" " on the 'Site information' panel"
        )
        if OSHelper.is_mac():
            time.sleep(1)  # to prevent clicks when pop-up is not fully loaded
        click(trackers_button_pattern)

        trackers_popup_displayed = exists(
            trackers_popup_title_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert trackers_popup_displayed, "Trackers popup window is displayed on screen"

        successfully_blocked_trackers_displayed = exists(
            blocked_tracker_label_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT
        )
        assert (
            successfully_blocked_trackers_displayed
        ), "A list of successfully blocked trackers is displayed."

        type(Key.ESC)

        tracking_protection_shield_displayed = exists(
            tracking_protection_shield_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            tracking_protection_shield_displayed
        ), "The tracking protection shield is displayed"

        click(tracking_protection_shield_pattern)

        disable_blocking_button_displayed = exists(
            disable_blocking_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            disable_blocking_button_displayed
        ), "The 'Site information' panel is displayed"

        click(disable_blocking_button_pattern)

        website_refreshes = exists(
            cnn_site_logo_pattern, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT
        )
        assert website_refreshes, "The website successfully refreshes"

        tracking_protection_shield_deactivated_displayed = exists(
            tracking_protection_shield_deactivated_pattern
        )
        assert tracking_protection_shield_deactivated_displayed, (
            "The 'tracking protection shield'"
            " is displayed as deactivated (strikethrough)"
        )

        move(tracking_protection_shield_deactivated_pattern)

        tracking_content_detected_message_displayed = exists(
            tracking_content_detected_message_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert tracking_content_detected_message_displayed, (
            "On hover, the tracking protection shield"
            " displays a 'Tracking content detected'"
            " tooltip message"
        )

        #  click on focus pattern as method restore_firefox_focus() doesn't work as expected
        website_displayed = exists(
            cnn_site_logo_pattern, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT
        )
        assert website_displayed, "The website is successfully displayed"

        restore_firefox_focus()

        cnn_blocked_content_displayed = scroll_until_pattern_found(
            cnn_blocked_content_pattern,
            type,
            (Key.PAGE_DOWN,),
            timeout=FirefoxSettings.FIREFOX_TIMEOUT,
        )
        assert cnn_blocked_content_displayed, (
            "Websites content that contain tracking elements"
            " are displayed on the page"
        )

        page_home()

        click(tracking_protection_shield_deactivated_pattern)

        site_information_panel_displayed = exists(
            enable_blocking_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            site_information_panel_displayed
        ), "The 'Site information' panel is displayed"

        trackers_button_available = exists(trackers_button_pattern)
        assert (
            trackers_button_available
        ), "'Trackers' button is displayed on the 'Site information' panel"

        click(trackers_button_pattern)

        list_of_active_trackers_displayed = not exists(
            trackers_icon_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            list_of_active_trackers_displayed
        ), "A list of active trackers is successfully displayed."

        type(Key.ESC)

        tracking_protection_shield_deactivated_displayed = exists(
            tracking_protection_shield_deactivated_pattern,
            FirefoxSettings.FIREFOX_TIMEOUT,
        )
        assert (
            tracking_protection_shield_deactivated_displayed
        ), "The tracking protection shield is displayed"

        click(tracking_protection_shield_deactivated_pattern)

        site_information_panel_displayed = exists(
            enable_blocking_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            site_information_panel_displayed
        ), "The 'Site information' panel is displayed"

        click(enable_blocking_button_pattern)

        website_refreshes = exists(
            cnn_site_logo_pattern, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT
        )
        assert website_refreshes, "The website successfully refreshes"

        tracking_protection_shield_displayed = exists(
            tracking_protection_shield_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            tracking_protection_shield_displayed
        ), "The tracking protection shield is displayed as active"

        hover(tracking_protection_shield_pattern)

        tracking_attempts_blocked_message_displayed = exists(
            tracking_attempts_blocked_message_pattern
        )
        assert tracking_attempts_blocked_message_displayed, (
            "On hover, the tracking protection shield"
            " displays a 'Tracking attempts blocked'"
            " tooltip message"
        )

        #  click on focus pattern as method restore_firefox_focus() doesn't work as expected
        website_displayed = exists(
            cnn_site_logo_pattern, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT
        )
        assert website_displayed, "The website is successfully displayed"

        restore_firefox_focus()

        cnn_blocked_content_not_displayed = scroll_until_pattern_found(
            cnn_blocked_content_pattern, type, (Key.PAGE_DOWN,), 10
        )
        assert cnn_blocked_content_not_displayed is False, (
            "Websites content that contain tracking elements"
            " are not displayed on the page"
        )

        click(tracking_protection_shield_pattern)

        site_information_panel_displayed = exists(
            trackers_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            site_information_panel_displayed
        ), "The 'Site information' panel is displayed"

        click(trackers_button_pattern)

        trackers_popup_displayed = exists(
            trackers_popup_title_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert trackers_popup_displayed, "Trackers popup window is displayed on screen"

        successfully_blocked_trackers_displayed = exists(
            blocked_tracker_label_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            successfully_blocked_trackers_displayed
        ), "A list of successfully blocked trackers is displayed."

        close_window()
