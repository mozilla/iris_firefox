# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Check the appearance of browser with Default Themes applied in Menu Bar.'
        self.test_case_id = '15267'
        self.test_suite_id = '494'
        self.locales = ['en-US']

    def run(self):
        open_addons()

        expected = exists(AboutAddons.THEMES, 10)
        assert_true(self, expected, 'Add-ons page successfully loaded.')

        click(AboutAddons.THEMES)

        expected = exists(AboutAddons.Themes.DARK_THEME, 10)
        assert_true(self, expected, 'Dark theme option found in the page.')

        expected = exists(AboutAddons.Themes.LIGHT_THEME, 10)
        assert_true(self, expected, 'Dark theme option found in the page.')

        expected = exists(AboutAddons.Themes.DEFAULT_THEME, 10)
        assert_true(self, expected, 'Dark theme option found in the page.')

        # Using the DEFAULT theme check that options from menu bar work correctly.
        click(AboutAddons.Themes.DEFAULT_THEME)

        expected = exists(AboutAddons.Themes.ENABLE_BUTTON, 5)
        assert_false(self, expected, 'ENABLE button NOT found in the page.')

        previous_tab()

        expected = exists(AboutAddons.Themes.IRIS_TAB_LIGHT_OR_DEFAULT_THEME, 10)
        assert_true(self, expected, 'Tab information is correctly displayed for DEFAULT theme.')

        select_zoom_menu_option(Option.ZOOM_IN)

        region = create_region_for_url_bar()
        expected = region.exists(LocationBar.URLBAR_ZOOM_BUTTON_110, Settings.FIREFOX_TIMEOUT)
        assert_true(self, expected, 'Zoom level successfully increased, zoom indicator found in the url bar.')

        restore_zoom()

        try:
            expected = region.wait_vanish(LocationBar.URLBAR_ZOOM_BUTTON_110, 5)
            assert_true(self, expected, 'Zoom indicator is displayed anymore in the url bar.')
        except FindError:
            raise FindError('Zoom indicator is still displayed in the url bar.')

        open_library()

        expected = exists(Library.BOOKMARKS_MENU, 10)
        assert_true(self, expected, 'Expand bookmarks menu button displayed properly.')

        click_window_control('close')

        # Enable the LIGHT theme and check that options from menu bar work correctly using the selected theme.
        next_tab()
        click(AboutAddons.THEMES)
        click(AboutAddons.Themes.LIGHT_THEME)

        expected = exists(AboutAddons.Themes.ENABLE_BUTTON, 10)
        assert_true(self, expected, 'ENABLE button found in the page.')

        click(AboutAddons.Themes.ENABLE_BUTTON)

        expected = exists(AboutAddons.Themes.DISABLE_BUTTON, 10)
        assert_true(self, expected, 'DISABLE button found in the page.')

        previous_tab()

        expected = exists(AboutAddons.Themes.IRIS_TAB_LIGHT_OR_DEFAULT_THEME, 10)
        assert_true(self, expected, 'LIGHT theme successfully applied.')

        select_zoom_menu_option(Option.ZOOM_IN)

        region = create_region_for_url_bar()
        expected = region.exists(LocationBar.URLBAR_ZOOM_BUTTON_110, Settings.FIREFOX_TIMEOUT)
        assert_true(self, expected, 'Zoom level successfully increased, zoom indicator found in the url bar.')

        restore_zoom()

        try:
            expected = region.wait_vanish(LocationBar.URLBAR_ZOOM_BUTTON_110, 5)
            assert_true(self, expected, 'Zoom indicator is displayed anymore in the url bar.')
        except FindError:
            raise FindError('Zoom indicator is still displayed in the url bar.')

        open_library()

        expected = exists(Library.BOOKMARKS_MENU, 10)
        assert_true(self, expected, 'Expand bookmarks menu button displayed properly.')

        click_window_control('close')

        # Enable the DARK theme and check that options from menu bar work correctly using the selected theme.
        next_tab()
        click(AboutAddons.THEMES)
        click(AboutAddons.Themes.DARK_THEME)

        expected = exists(AboutAddons.Themes.ENABLE_BUTTON, 10)
        assert_true(self, expected, 'ENABLE button found in the page.')

        click(AboutAddons.Themes.ENABLE_BUTTON)

        expected = exists(AboutAddons.Themes.DISABLE_BUTTON, 10)
        assert_true(self, expected, 'DISABLE button found in the page.')

        previous_tab()

        expected = exists(AboutAddons.Themes.IRIS_TAB_DARK_THEME, 10)
        assert_true(self, expected, 'LIGHT theme successfully applied.')

        open_library()

        expected = exists(Library.BOOKMARKS_MENU, 10)
        assert_true(self, expected, 'Expand bookmarks menu button displayed properly.')

        click_window_control('close')
