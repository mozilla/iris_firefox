# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'There are no glitches in tab layout.'
        self.test_case_id = '15268'
        self.test_suite_id = '494'
        self.locales = ['en-US']

    def run(self):
        mozilla_tab_not_focused = Pattern('mozilla_tab_not_focused.png')
        mozilla_tab_not_focused_light_theme = Pattern('mozilla_tab_not_focused_light_theme.png')
        mozilla_hover = Pattern('mozilla_hover.png').similar(0.7)
        mozilla_hover_dark_theme = Pattern('mozilla_hover_dark_theme.png').similar(0.7)
        close_tab_button = Pattern('close_tab_button.png')
        close_tab_button_dark_theme = Pattern('close_tab_button_dark_theme.png')
        close_tab_hover = Pattern('close_tab_hover.png').similar(0.7)
        close_tab_hover_dark_theme = Pattern('close_tab_hover_dark_theme.png').similar(0.7)

        open_addons()
        previous_tab()
        close_tab()

        expected = exists(AboutAddons.THEMES, 10)
        assert_true(self, expected, 'Add-ons page successfully loaded.')

        click(AboutAddons.THEMES)

        expected = exists(AboutAddons.Themes.DARK_THEME, 10)
        assert_true(self, expected, 'Dark theme option found in the page.')

        expected = exists(AboutAddons.Themes.LIGHT_THEME, 10)
        assert_true(self, expected, 'Dark theme option found in the page.')

        expected = exists(AboutAddons.Themes.DEFAULT_THEME, 10)
        assert_true(self, expected, 'Dark theme option found in the page.')

        # DEFAULT theme.
        click(AboutAddons.Themes.DEFAULT_THEME)

        expected = exists(AboutAddons.Themes.ENABLE_BUTTON, 5)
        assert_false(self, expected, 'ENABLE button NOT found in the page.')

        # Open at least 10 tabs and load pages in each one.
        for i in range(10):
            new_tab()
            navigate(LocalWeb.MOZILLA_TEST_SITE)
            expected = exists(LocalWeb.MOZILLA_LOGO, 120)
            assert_true(self, expected, 'Mozilla page loaded successfully.')

        max_attempts = 9

        while max_attempts > 0:
            expected = exists(mozilla_tab_not_focused, 3)

            if expected:
                tab = find(mozilla_tab_not_focused)
                region = Region(tab.x, tab.y - 10, 220, 80)
                region.hover(tab)

                expected = region.exists(mozilla_hover, 10)
                assert_true(self, expected, 'Mozilla page is hovered.')

                region.click(tab)

                expected = region.exists(close_tab_button, 10)
                assert_true(self, expected, 'Close tab button is visible.')

                region.hover(close_tab_button)

                expected = exists(close_tab_hover, 10)
                assert_true(self, expected, 'Close button is hovered.')

                region.click(close_tab_button.similar(0.7))
                max_attempts -= 1
            else:
                max_attempts = 0

        close_tab()

        # LIGHT theme.
        expected = exists(AboutAddons.THEMES, 10)
        assert_true(self, expected, 'Add-ons page is in focus.')

        click(AboutAddons.THEMES)

        click(AboutAddons.Themes.LIGHT_THEME)

        expected = exists(AboutAddons.Themes.ENABLE_BUTTON, 5)
        assert_true(self, expected, 'ENABLE button found in the page.')

        click(AboutAddons.Themes.ENABLE_BUTTON)

        expected = exists(AboutAddons.Themes.DISABLE_BUTTON, 10)
        assert_true(self, expected, 'DISABLE button found in the page.')

        # Open at least 10 tabs and load pages in each one.
        for i in range(10):
            new_tab()
            navigate(LocalWeb.MOZILLA_TEST_SITE)
            expected = exists(LocalWeb.MOZILLA_LOGO, 120)
            assert_true(self, expected, 'Mozilla page loaded successfully.')

        max_attempts = 9

        while max_attempts > 0:
            expected = exists(mozilla_tab_not_focused_light_theme, 3)

            if expected:
                tab = find(mozilla_tab_not_focused_light_theme)
                region = Region(tab.x, tab.y - 10, 220, 80)
                hover(tab)

                expected = region.exists(mozilla_hover, 10)
                assert_true(self, expected, 'Mozilla page is hovered.')

                region.click(tab)

                expected = region.exists(close_tab_button, 10)
                assert_true(self, expected, 'Close tab button is visible.')

                region.hover(close_tab_button)

                expected = exists(close_tab_hover, 10)
                assert_true(self, expected, 'Close button is hovered.')

                region.click(close_tab_button.similar(0.7))
                max_attempts -= 1
            else:
                max_attempts = 0

        close_tab()

        # DARK theme.
        expected = exists(AboutAddons.THEMES, 10)
        assert_true(self, expected, 'Add-ons page is in focus.')

        click(AboutAddons.THEMES)

        click(AboutAddons.Themes.DARK_THEME)

        expected = exists(AboutAddons.Themes.ENABLE_BUTTON, 10)
        assert_true(self, expected, 'ENABLE button found in the page.')

        click(AboutAddons.Themes.ENABLE_BUTTON)

        expected = exists(AboutAddons.Themes.DISABLE_BUTTON, 10)
        assert_true(self, expected, 'DISABLE button found in the page.')

        # Open at least 10 tabs and load pages in each one.
        for i in range(10):
            new_tab()
            navigate(LocalWeb.MOZILLA_TEST_SITE)
            expected = exists(LocalWeb.MOZILLA_LOGO, 120)
            assert_true(self, expected, 'Mozilla page loaded successfully.')

        max_attempts = 9

        while max_attempts > 0:
            expected = exists(mozilla_tab_not_focused, 3)

            if expected:
                tab = find(mozilla_tab_not_focused)
                region = Region(tab.x, tab.y - 10, 220, 80)
                hover(tab)

                expected = region.exists(mozilla_hover_dark_theme, 10)
                assert_true(self, expected, 'Mozilla page is hovered.')

                region.click(tab)

                expected = region.exists(close_tab_button_dark_theme, 10)
                assert_true(self, expected, 'Close tab button is visible.')

                region.hover(close_tab_button_dark_theme)

                expected = exists(close_tab_hover_dark_theme, 10)
                assert_true(self, expected, 'Close button is hovered.')

                region.click(close_tab_button_dark_theme.similar(0.7))
                max_attempts -= 1
            else:
                max_attempts = 0

        close_tab()
