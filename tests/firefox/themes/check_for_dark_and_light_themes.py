# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Check for Dark and Light themes.",
        locale=["en-US"],
        test_case_id="15266",
        test_suite_id="494"
    )
    def run(self, firefox):
        for i in range(2):
            if i == 1:
                new_private_window()
                if OSHelper.is_linux():
                    navigate("about:addons")
            open_hamburger_menu('Add-ons')

            expected = exists(AboutAddons.THEMES, FirefoxSettings.FIREFOX_TIMEOUT)
            assert expected, "Add-ons page couldn't be loaded."

            click(AboutAddons.THEMES)

            expected = exists(AboutAddons.Themes.DEFAULT_THEME, FirefoxSettings.FIREFOX_TIMEOUT)
            assert expected, "Default theme option not found in the page."

            expected = exists(AboutAddons.Themes.DARK_THEME, FirefoxSettings.FIREFOX_TIMEOUT)
            assert expected, "Dark theme option not found in the page."

            if OSHelper.is_mac():
                click(Pattern("disabled_theme_header.png"))
                type(Key.DOWN)
            expected = exists(AboutAddons.Themes.LIGHT_THEME, FirefoxSettings.FIREFOX_TIMEOUT)
            assert expected, "Light theme option not found in the page."

        close_window()
