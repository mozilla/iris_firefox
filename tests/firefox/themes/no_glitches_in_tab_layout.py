# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='There are no glitches in tab layout.',
        locale=['en-US'],
        test_case_id='15268',
        test_suite_id='494'
    )
    def run(self, firefox):
        mozilla_tab_not_focused = Pattern('mozilla_tab_not_focused.png').similar(0.7)
        mozilla_tab_not_focused_light_theme = Pattern('mozilla_tab_not_focused_light_theme.png').similar(0.7)
        mozilla_hover = Pattern('mozilla_hover.png').similar(0.7)
        mozilla_hover_dark_theme = Pattern('mozilla_hover_dark_theme.png').similar(0.7)
        close_tab_button = Pattern('close_tab_button.png').similar(0.7)
        close_tab_button_dark_theme = Pattern('close_tab_button_dark_theme.png').similar(0.7)
        close_tab_hover = Pattern('close_tab_hover.png').similar(0.7)
        close_tab_hover_dark_theme = Pattern('close_tab_hover_dark_theme.png')

        open_addons()
        previous_tab()
        close_tab()

        expected = exists(AboutAddons.THEMES, 10)
        assert expected is True, 'Add-ons page successfully loaded.'

        click(AboutAddons.THEMES)

        expected = exists(AboutAddons.Themes.DARK_THEME, 10)
        assert expected is True, 'Dark theme option found in the page.'

        expected = exists(AboutAddons.Themes.LIGHT_THEME, 10)
        assert expected is True, 'Dark theme option found in the page.'

        expected = exists(AboutAddons.Themes.DEFAULT_THEME, 10)
        assert expected is True, 'Dark theme option found in the page.'

        # DEFAULT theme.
        click(AboutAddons.Themes.DEFAULT_THEME)

        expected = exists(AboutAddons.Themes.ENABLE_BUTTON, 5)
        assert expected is True, 'ENABLE button NOT found in the page.'

        # Open at least 10 tabs and load pages in each one.
        for i in range(10):
            new_tab()
            navigate(LocalWeb.MOZILLA_TEST_SITE)
            expected = exists(LocalWeb.MOZILLA_LOGO, 120)
            assert expected is True, 'Mozilla page loaded successfully.'

        max_attempts = 9

        while max_attempts > 0:
            expected = exists(mozilla_tab_not_focused, 3)

            if expected:
                tab = find(mozilla_tab_not_focused)
                region = Region(tab.x - 10, tab.y - 10, 220, 80)
                region.hover(mozilla_tab_not_focused, align=Alignment.CENTER)

                expected = exists(mozilla_hover, 10)
                assert expected is True, 'Mozilla page is hovered.'

                region.click(mozilla_tab_not_focused)

                expected = exists(close_tab_button, 10)
                assert expected is True, 'Close tab button is visible.'

                hover(close_tab_button, align=Alignment.CENTER)

                expected = exists(close_tab_hover, 10)
                assert expected is True, 'Close button is hovered.'

                region.click(close_tab_button)
                time.sleep(Settings.DEFAULT_UI_DELAY)

                max_attempts -= 1
            else:
                max_attempts = 0

        close_tab()

        # LIGHT theme.
        expected = exists(AboutAddons.THEMES, 10)
        assert expected is True, 'Add-ons page is in focus.'

        click(AboutAddons.THEMES)

        click(AboutAddons.Themes.LIGHT_THEME)

        expected = exists(AboutAddons.Themes.ENABLE_BUTTON, 5)
        assert expected is True, 'ENABLE button found in the page.'

        click(AboutAddons.Themes.ENABLE_BUTTON)

        expected = exists(AboutAddons.Themes.DISABLE_BUTTON, 10)
        assert expected is True, 'DISABLE button found in the page.'

        # Open at least 10 tabs and load pages in each one.
        for i in range(10):
            new_tab()
            navigate(LocalWeb.MOZILLA_TEST_SITE)
            expected = exists(LocalWeb.MOZILLA_LOGO, 120)
            assert expected is True, 'Mozilla page loaded successfully.'

        max_attempts = 9

        while max_attempts > 0:
            expected = exists(mozilla_tab_not_focused_light_theme, 3)

            if expected:
                tab = find(mozilla_tab_not_focused_light_theme)
                region = Region(tab.x, tab.y - 10, 220, 80)
                region.hover(mozilla_tab_not_focused_light_theme, align=Alignment.CENTER)

                expected = exists(mozilla_hover, 10)
                assert expected is True, 'Mozilla page is hovered.'

                region.click(mozilla_tab_not_focused_light_theme)

                expected = exists(close_tab_button, 10)
                assert expected is True, 'Close tab button is visible.'

                hover(close_tab_button, align=Alignment.CENTER)

                expected = exists(close_tab_hover, 10)
                assert expected is True, 'Close button is hovered.'

                region.click(close_tab_button.similar(0.6))
                time.sleep(Settings.DEFAULT_UI_DELAY)

                max_attempts -= 1
            else:
                max_attempts = 0

        close_tab()

        # DARK theme.
        expected = exists(AboutAddons.THEMES, 10)
        assert expected is True, 'Add-ons page is in focus.'

        click(AboutAddons.THEMES)

        click(AboutAddons.Themes.DARK_THEME)

        expected = exists(AboutAddons.Themes.ENABLE_BUTTON, 10)
        assert expected is True, 'ENABLE button found in the page.'

        click(AboutAddons.Themes.ENABLE_BUTTON)

        expected = exists(AboutAddons.Themes.DISABLE_BUTTON, 10)
        assert expected is True, 'DISABLE button found in the page.'

        # Open at least 10 tabs and load pages in each one.
        for i in range(10):
            new_tab()
            navigate(LocalWeb.MOZILLA_TEST_SITE)
            expected = exists(LocalWeb.MOZILLA_LOGO, 120)
            assert expected is True, 'Mozilla page loaded successfully.'

        max_attempts = 9

        while max_attempts > 0:
            expected = exists(mozilla_tab_not_focused, 3)

            if expected:
                tab = find(mozilla_tab_not_focused)
                region = Region(tab.x - 10, tab.y - 10, 220, 80)
                region.hover(mozilla_tab_not_focused, align=Alignment.CENTER)

                expected = exists(mozilla_hover_dark_theme, 10)
                assert expected is True, 'Mozilla page is hovered.'

                region.click(mozilla_tab_not_focused)

                expected = exists(close_tab_button_dark_theme, 10)
                assert expected is True, 'Close tab button is visible.'

                hover(close_tab_button_dark_theme, align=Alignment.CENTER)

                expected = exists(close_tab_hover_dark_theme, 10)
                assert expected is True, 'Close button is hovered.'

                region.click(close_tab_button_dark_theme)
                time.sleep(Settings.DEFAULT_UI_DELAY)

                max_attempts -= 1
            else:
                max_attempts = 0

        close_tab()
