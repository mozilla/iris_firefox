# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Dragging tabs is completely broken",
        locale=["en-US"],
        test_case_id="135373",
        test_suite_id="2103",
    )
    def run(self, firefox):
        preferences_tab_icon_pattern = Pattern("preferences_tab_icon.png")
        new_tab_icon_pattern = Pattern("new_tab_icon.png")
        mozilla_tab_icon_pattern = Pattern("mozilla_tab_icon.png")
        drag_and_drop_duration = 2
        tab_icon_list = [mozilla_tab_icon_pattern,
                         preferences_tab_icon_pattern,
                         new_tab_icon_pattern]

        for _ in range(30):
            new_tab()
            top_site_exists = exists(Utils.TOP_SITES, FirefoxSettings.FIREFOX_TIMEOUT)
            assert top_site_exists, "New tab couldn't open."

        navigate("about:preferences#privacy")
        about_preferences_privacy_address_exist = exists(LocalWeb.ABOUT_PREFERENCES_PRIVACY_ADDRESS,
                                                         FirefoxSettings.FIREFOX_TIMEOUT)
        assert about_preferences_privacy_address_exist, "About preference privacy page couldn't load."

        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        mozilla_logo_exists = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_logo_exists, "Mozilla page couldn't load."

        mozilla_tab_pattern_exists = exists(mozilla_tab_icon_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_tab_pattern_exists, "Could not find mozilla tab"

        mozilla_tab_width, mozilla_tab_height = mozilla_tab_icon_pattern.get_size()
        mozilla_tab_location = find(mozilla_tab_icon_pattern)

        tab_bar_region = Region(mozilla_tab_location.x - mozilla_tab_width * 8,
                                mozilla_tab_location.y - mozilla_tab_width / 4,
                                mozilla_tab_width * 11,
                                mozilla_tab_height * 1.5
                                )
        self.tab_icon_exists(tab_icon_list, tab_bar_region)

        mozilla_tab_icon_location = find(mozilla_tab_icon_pattern, region=tab_bar_region)
        new_tab_icon_location = find(new_tab_icon_pattern, region=tab_bar_region)

        drag_drop(mozilla_tab_icon_location, new_tab_icon_location, duration=drag_and_drop_duration)

        self.tab_icon_exists(tab_icon_list, tab_bar_region)

        drop_new_tab_icon_location = find(new_tab_icon_pattern, region=tab_bar_region)
        drop_preferences_tab_icon_location = find(preferences_tab_icon_pattern, region=tab_bar_region)
        drop_mozilla_tab_icon_location = find(mozilla_tab_icon_pattern, region=tab_bar_region)

        # comparing the drop location of the tabs to check whether tabs are correctly reordered or not
        tab_reorder = (drop_mozilla_tab_icon_location.x < drop_new_tab_icon_location.x) and (
                    drop_preferences_tab_icon_location.x > drop_mozilla_tab_icon_location.x)
        assert tab_reorder, "Tabs are not correctly reordered to where the mouse pointer."

    @staticmethod
    def tab_icon_exists(tab_icon_list: list, region: Region):
        """Check if Pattern or image exists.

        :param tab_icon_list: list of tab icon patterns.
        :param region: Rectangle tab bar region.
        :return: None.
        """
        for tab in tab_icon_list:
            tab_icon_name = tab.get_filename().split('.')[0].replace('_', ' ')
            mozilla_tab_icon_pattern_exist = exists(tab, FirefoxSettings.FIREFOX_TIMEOUT, region)
            assert mozilla_tab_icon_pattern_exist, f"Could not find {tab_icon_name} in given region."
