# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="There are no UI glitches pinned tabs layout",
        locale=["en-US"],
        test_case_id="15270",
        test_suite_id="494",
    )
    def run(self, firefox):
        pref_tab_pattern = Pattern("preferences_tab_icon.png")
        robot_tab_pattern = Pattern("robot_tab_icon.png")
        addon_pattern = Pattern("addon_tab_icon.png")
        protections_tab_pattern = Pattern("protections_tab_icon.png")
        sync_tab_pattern = Pattern("sync_tab_icon.png")
        debugging_tab_pattern = Pattern("debugging_tab_icon.png")
        logins_tab_pattern = Pattern("logins_tab_icon.png")
        performance_tab_pattern = Pattern("performance_tab_icon.png")
        wiki_tab_pattern = Pattern("wiki_tab_icon.png")
        new_tab_pattern = Pattern("new_tab_icon.png")
        facebook_tab_pattern = Pattern("facebook_tab_icon.png")
        poket_dark_tab_pattern = Pattern("poket_tab_icon.png")
        mdn_dark_tab_pattern = Pattern("mdn_tab_icon.png")
        mozilla_dark_tab_pattern = Pattern("mozilla_org_tab_icon.png")
        iris_tab_pattern = Pattern("iris_tab_icon.png")

        drag_drop_duration = 2

        site_url = [LocalWeb.POCKET_TEST_SITE,
                    LocalWeb.SOAP_WIKI_TEST_SITE,
                    "about:addons",
                    "about:preferences",
                    "about:robots",
                    "about:protections",
                    "about:sync-log",
                    "about:debugging#/setup",
                    "about:logins",
                    "about:performance",
                    "about:newtab",
                    "https://www.facebook.com/",
                    "https://developer.mozilla.org/en-US/",
                    "https://www.mozilla.org/en-US/"
                    ]

        tab_images = [poket_dark_tab_pattern,
                      wiki_tab_pattern,
                      addon_pattern,
                      pref_tab_pattern,
                      robot_tab_pattern,
                      protections_tab_pattern,
                      sync_tab_pattern,
                      debugging_tab_pattern,
                      logins_tab_pattern,
                      performance_tab_pattern,
                      new_tab_pattern,
                      facebook_tab_pattern,
                      mdn_dark_tab_pattern,
                      mozilla_dark_tab_pattern,
                      ]

        open_hamburger_menu('Add-ons')
        theme_exists = exists(AboutAddons.THEMES)
        if theme_exists:
            click(AboutAddons.THEMES)

        default_theme_exists = exists(AboutAddons.Themes.DEFAULT_THEME, FirefoxSettings.FIREFOX_TIMEOUT)
        assert default_theme_exists, "Default theme option not found in Addons page."

        dark_theme_exists = exists(AboutAddons.Themes.DARK_THEME, FirefoxSettings.FIREFOX_TIMEOUT)
        assert dark_theme_exists, "Dark theme option not found in Addons page."

        if OSHelper.is_mac():
            click(Pattern("disabled_theme_header.png"))
            type(Key.DOWN)
        light_theme_exists = exists(AboutAddons.Themes.LIGHT_THEME, FirefoxSettings.FIREFOX_TIMEOUT)
        assert light_theme_exists, "Light theme option not found in Addons page."

        theme_location = find(AboutAddons.Themes.DARK_THEME)
        theme_width, theme_height = AboutAddons.Themes.DARK_THEME.get_size()
        theme_region = Region(0,
                              theme_location.y - theme_height / 2,
                              Screen.SCREEN_WIDTH,
                              theme_height * 2)
        enable_button_exists = exists(AboutAddons.Themes.ENABLE_BUTTON, FirefoxSettings.FIREFOX_TIMEOUT,
                                        theme_region)
        assert enable_button_exists, "Enable button does not exists in dark theme region."
        click(AboutAddons.Themes.ENABLE_BUTTON, region=theme_region)

        dark_theme_exists = exists(AboutAddons.Themes.IRIS_TAB_DARK_THEME, FirefoxSettings.FIREFOX_TIMEOUT)
        assert dark_theme_exists, "Could not apply dark theme successfully"
        close_tab()

        iris_tab_pattern_exists = exists(iris_tab_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert iris_tab_pattern_exists, "Could not find dark Iris tab in the tab bar"

        iris_tab_width, iris_tab_height = iris_tab_pattern.get_size()
        iris_tab_location = find(iris_tab_pattern)

        tab_region_area = 0
        for site, tab_image in zip(site_url, tab_images):
            new_tab()
            navigate(site)
            tab_exist = exists(tab_image, FirefoxSettings.SITE_LOAD_TIMEOUT)
            tab_name = tab_image.get_filename().split('.')[0].replace("_", " ").replace("icon","")
            assert tab_exist, f"Could not load {tab_name} successfully."
            tab_region_area += 2
            pinned_region = Region(iris_tab_location.x - iris_tab_width / 4,
                                   iris_tab_location.y - iris_tab_height / 4,
                                   iris_tab_width * tab_region_area,
                                   iris_tab_height * 1.5
                                   )
            self.pin_unpin_tab(tab_image, pinned_region)

        self.pin_unpin_tab(iris_tab_pattern, pinned_region)

        pined_iris_tab_location = find(iris_tab_pattern)
        pined_debugging_tab_location = find(debugging_tab_pattern)
        drag_drop(pined_iris_tab_location, pined_debugging_tab_location, duration=drag_drop_duration)

        pinned_iris_tab_exists = exists(iris_tab_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=pinned_region)
        assert pinned_iris_tab_exists, "Could not find pinned iris tab in the given tab bar region"

        pined_debugging_tab_exist = exists(debugging_tab_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=pinned_region)
        assert pined_debugging_tab_exist, "Could not find pinned debugging tab in the given tab bar region"

        sync_tab_tab_exist = exists(sync_tab_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=pinned_region)
        assert sync_tab_tab_exist, "Could not find pinned sync tab in the given tab bar region"

        drop_iris_tab_location = find(iris_tab_pattern)
        drop_debugging_tab_location = find(debugging_tab_pattern)
        sync_tab_location = find(sync_tab_pattern)

        drop_tab_compare = (drop_iris_tab_location.x < drop_debugging_tab_location.x) and \
                           (drop_iris_tab_location.x > sync_tab_location.x)

        assert drop_tab_compare, "Could not change the position of the pinned iris tab properly"

        # unpin pinned iris tab
        self.pin_unpin_tab(iris_tab_pattern, pinned_region)

        dark_iris_tab_exist = exists(AboutAddons.Themes.IRIS_TAB_DARK_THEME, FirefoxSettings.FIREFOX_TIMEOUT)
        assert dark_iris_tab_exist, "Could unpin iris tab successfully"

    @staticmethod
    def pin_unpin_tab(tab_pattern: Pattern, tab_bar_region: Region):
        """Pin or unpin Tabs.
        :param tab_pattern: Tab icon pattern.
        :param tab_bar_region: Tab bar region to be pinned.
        :return: None.
        """
        right_click(tab_pattern)
        if OSHelper.is_windows():
            type(text="p", modifier=KeyModifier.SHIFT)
        else:
            type(text="p",modifier=KeyModifier.CTRL)
        tab_name = tab_pattern.get_filename().split('.')[0].replace("_", " ").replace("icon","")
        pinned_tab_exist = exists(tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT, region=tab_bar_region)
        assert pinned_tab_exist, f"Could not pin {tab_name} successfully in the given tab bar region."
