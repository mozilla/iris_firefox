# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Check the appearance of browser with Default Themes applied in Menu Bar.',
        locale=['en-US'],
        test_case_id='15267',
        test_suite_id='494'
    )
    def run(self, firefox):
        open_addons()

        expected = exists(AboutAddons.THEMES, 10)
        assert expected, 'Add-ons page successfully loaded.'

        click(AboutAddons.THEMES)

        expected = exists(AboutAddons.Themes.DARK_THEME, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Dark theme option found in the page.'

        expected = exists(AboutAddons.Themes.LIGHT_THEME, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Light theme option found in the page.'

        expected = exists(AboutAddons.Themes.DEFAULT_THEME, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Default theme option found in the page.'

        # Using the DEFAULT theme check that options from menu bar work correctly.
        click(AboutAddons.Themes.DEFAULT_THEME)
        time.sleep(Settings.DEFAULT_UI_DELAY)

        action_can_be_performed = exists(AboutAddons.Themes.ACTION_BUTTON)
        assert action_can_be_performed is False, 'Theme can be enabled/disabled.'

        previous_tab()

        expected = exists(AboutAddons.Themes.IRIS_TAB_LIGHT_OR_DEFAULT_THEME, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Tab information is correctly displayed for DEFAULT theme.'

        open_library()

        expected = exists(Library.BOOKMARKS_MENU, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Expand bookmarks menu button displayed properly.'

        click_window_control('close')

        # Enable the LIGHT theme and check that options from menu bar work correctly using the selected theme.
        next_tab()
        click(AboutAddons.THEMES)
        time.sleep(Settings.DEFAULT_UI_DELAY)
        click(AboutAddons.Themes.LIGHT_THEME)

        action_can_be_performed = exists(AboutAddons.Themes.ACTION_BUTTON)
        assert action_can_be_performed, 'Theme can be enabled.'
        click(AboutAddons.Themes.ACTION_BUTTON)

        expected = exists(AboutAddons.Themes.ENABLE_BUTTON, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'ENABLE button found in the page.'

        click(AboutAddons.Themes.ENABLE_BUTTON)

        action_can_be_performed = exists(AboutAddons.Themes.ACTION_BUTTON)
        assert action_can_be_performed, 'Theme can be disabled.'
        click(AboutAddons.Themes.ACTION_BUTTON)

        expected = exists(AboutAddons.Themes.DISABLE_BUTTON, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'DISABLE button found in the page.'

        previous_tab()

        expected = exists(AboutAddons.Themes.IRIS_TAB_LIGHT_OR_DEFAULT_THEME, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'LIGHT theme successfully applied.'

        open_library()

        expected = exists(Library.BOOKMARKS_MENU, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Expand bookmarks menu button displayed properly.'

        click_window_control('close')

        # Enable the DARK theme and check that options from menu bar work correctly using the selected theme.
        next_tab()
        click(AboutAddons.THEMES)
        click(AboutAddons.Themes.DARK_THEME)

        action_can_be_performed = exists(AboutAddons.Themes.ACTION_BUTTON)
        assert action_can_be_performed, 'Theme can be enabled.'
        click(AboutAddons.Themes.ACTION_BUTTON)

        expected = exists(AboutAddons.Themes.ENABLE_BUTTON, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'ENABLE button found in the page.'

        click(AboutAddons.Themes.ENABLE_BUTTON)

        action_can_be_performed = exists(AboutAddons.Themes.ACTION_BUTTON)
        assert action_can_be_performed, 'Theme can be disabled.'
        click(AboutAddons.Themes.ACTION_BUTTON)

        expected = exists(AboutAddons.Themes.DISABLE_BUTTON, 10)
        assert expected, 'DISABLE button found in the page.'

        previous_tab()

        expected = exists(AboutAddons.Themes.IRIS_TAB_DARK_THEME, 10)
        assert expected, 'DARK theme successfully applied.'

        open_library()

        expected = exists(Library.BOOKMARKS_MENU, 10)
        assert expected, 'Expand bookmarks menu button displayed properly.'

        click_window_control('close')
