# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Bug - DnD tabs broken in Nightly run",
        locale=["en-US"],
        test_case_id="175217",
        test_suite_id="2103",
    )
    def run(self, firefox):
        new_tab_image_pattern = Pattern("new_tab_icon.png")
        mozilla_tab_pattern = Pattern("mozilla_tab.png")
        unopened_mozilla_tab_pattern = Pattern("unopened_mozilla_tab.png")
        home_preference_pattern = Pattern("home_preference.png")
        downloads_tab_url = Pattern("downloads_tab_url.png")
        downloads_tab_pattern = Pattern("downloads_tab.png")
        pref_tab_pattern = Pattern("pref_tab.png")

        navigate("about:preferences#home")
        preference_home_tab_image = exists(home_preference_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert preference_home_tab_image, "preference home page could not load successfully"
        new_tab()
        navigate("about:downloads")
        config_tab_image = (downloads_tab_url, FirefoxSettings.FIREFOX_TIMEOUT)
        assert config_tab_image, "Downloads page could not load successfully"
        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        new_tab_image = exists(mozilla_tab_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert new_tab_image, "Mozilla tab could not open successfully"

        tab_location = find(mozilla_tab_pattern)
        drop_location = find(downloads_tab_pattern)
        drag_drop(tab_location, drop_location)
        pref_tab_location = find(pref_tab_pattern)
        mozilla_tab_location = find(mozilla_tab_pattern)
        downloads_tab_location = find(downloads_tab_pattern)

        pref_tab_width, pref_tab_height = pref_tab_pattern.get_size()
        first_reorder_window_region = Region(pref_tab_location.x - pref_tab_width/4,
                                             pref_tab_location.y - pref_tab_height/4,
                                             pref_tab_width * 3.5,
                                             pref_tab_height * 1.5
                                             )

        pattern_exists = exists(mozilla_tab_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT, first_reorder_window_region)
        assert pattern_exists, "Mozilla tab pattern not found"

        # comparing mozilla tab is in between pref_tab and downloads_tab
        reorder_tab = (mozilla_tab_location.x < downloads_tab_location.x) and \
                      (mozilla_tab_location.x > pref_tab_location.x)
        assert reorder_tab, "All the Tabs are not correctly reordered"

        new_window()
        new_tab_image = exists(new_tab_image_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert new_tab_image, "Could not open new window"

        # drag the new window down
        controls_location = find(new_tab_image_pattern)
        x_coord = controls_location.x
        y_coord = controls_location.y
        drag_start = Location(x_coord + 400, y_coord+5)
        drag_end = Location(x_coord + 700, y_coord + 200)
        drag_drop(drag_start, drag_end)


        tab_location = find(new_tab_image_pattern)
        drop_location = find(mozilla_tab_pattern)
        drag_drop(tab_location, drop_location, duration=0.5)
        pref_tab_width, pref_tab_height = pref_tab_pattern.get_size()

        second_reorder_window_region = Region(pref_tab_location.x-pref_tab_width/4,
                                              pref_tab_location.y-pref_tab_height/4,
                                              pref_tab_width * 3.5,
                                              pref_tab_height*1.5
                                              )

        new_tab_image = exists(new_tab_image_pattern, FirefoxSettings.FIREFOX_TIMEOUT, second_reorder_window_region)
        assert new_tab_image, "Could not open new tab"
        mozilla_tab_location = find(unopened_mozilla_tab_pattern)
        new_tab_location = find(new_tab_image_pattern)

        # comparing new_tab_location is in between pref_tab and mozilla_tab_location
        tab_reordered = (new_tab_location.x < mozilla_tab_location.x) and (new_tab_location.x > pref_tab_location.x)
        assert tab_reordered, "Tab couldn't be reordered from second window to first window"
