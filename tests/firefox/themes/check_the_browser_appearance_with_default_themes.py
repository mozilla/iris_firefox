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
        assert expected is True, 'Add-ons page successfully loaded.'

        click(AboutAddons.THEMES)

        expected = exists(AboutAddons.Themes.DARK_THEME, 10)
        assert expected is True, 'Dark theme option found in the page.'

        expected = exists(AboutAddons.Themes.LIGHT_THEME, 10)
        assert expected is True, 'Dark theme option found in the page.'

        expected = exists(AboutAddons.Themes.DEFAULT_THEME, 10)
        assert expected is True, 'Dark theme option found in the page.'

        # Using the DEFAULT theme check that options from menu bar work correctly.
        click(AboutAddons.Themes.DEFAULT_THEME)
        time.sleep(Settings.DEFAULT_UI_DELAY)

        expected = exists(AboutAddons.Themes.ENABLE_BUTTON, 5)
        assert expected is not True, 'ENABLE button NOT found in the page.'

        previous_tab()

        expected = exists(AboutAddons.Themes.IRIS_TAB_LIGHT_OR_DEFAULT_THEME, 10)
        assert expected is True, 'Tab information is correctly displayed for DEFAULT theme.'

        open_library()

        expected = exists(Library.BOOKMARKS_MENU, 10)
        assert expected is True, 'Expand bookmarks menu button displayed properly.'

        click_window_control('close')

        # Enable the LIGHT theme and check that options from menu bar work correctly using the selected theme.
        next_tab()
        click(AboutAddons.THEMES)
        time.sleep(Settings.DEFAULT_UI_DELAY)
        click(AboutAddons.Themes.LIGHT_THEME)

        expected = exists(AboutAddons.Themes.ENABLE_BUTTON, 10)
        assert expected is True, 'ENABLE button found in the page.'

        click(AboutAddons.Themes.ENABLE_BUTTON)

        expected = exists(AboutAddons.Themes.DISABLE_BUTTON, 10)
        assert expected is True, 'DISABLE button found in the page.'

        previous_tab()

        expected = exists(AboutAddons.Themes.IRIS_TAB_LIGHT_OR_DEFAULT_THEME, 10)
        assert expected is True, 'LIGHT theme successfully applied.'

        open_library()

        expected = exists(Library.BOOKMARKS_MENU, 10)
        assert expected is True, 'Expand bookmarks menu button displayed properly.'

        click_window_control('close')

        # Enable the DARK theme and check that options from menu bar work correctly using the selected theme.
        next_tab()
        click(AboutAddons.THEMES)
        click(AboutAddons.Themes.DARK_THEME)

        expected = exists(AboutAddons.Themes.ENABLE_BUTTON, 10)
        assert expected is True, 'ENABLE button found in the page.'

        click(AboutAddons.Themes.ENABLE_BUTTON)

        expected = exists(AboutAddons.Themes.DISABLE_BUTTON, 10)
        assert expected is True, 'DISABLE button found in the page.'

        previous_tab()

        expected = exists(AboutAddons.Themes.IRIS_TAB_DARK_THEME, 10)
        assert expected is True, 'LIGHT theme successfully applied.'

        open_library()

        expected = exists(Library.BOOKMARKS_MENU, 10)
        assert expected is True, 'Expand bookmarks menu button displayed properly.'

        click_window_control('close')
