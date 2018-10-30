# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This is a test case that checks the zoom controls on toolbar.'
        self.test_case_id = '7443'
        self.test_suite_id = '242'
        self.locales = ['en-US']

    def run(self):
        url = LocalWeb.FIREFOX_TEST_SITE
        url_bar_default_zoom_level_pattern = Pattern('url_bar_default_zoom_level.png')
        zoom_controls_customize_page_pattern = Pattern('zoom_controls_customize_page.png')
        default_zoom_level_toolbar_customize_page_pattern = Pattern('default_zoom_level_toolbar_customize_page.png')
        default_zoom_level_toolbar_pattern = LocationBar.DEFAULT_ZOOM_LEVEL
        zoom_control_toolbar_decrease_pattern = Pattern('zoom_control_toolbar_decrease.png')
        zoom_control_toolbar_increase_pattern = Pattern('zoom_control_toolbar_increase.png')
        zoom_control_90_pattern = Pattern('zoom_control_90.png')
        zoom_control_110_pattern = Pattern('zoom_control_110.png')
        toolbar_pattern = Pattern('toolbar.png')

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        region = create_region_for_url_bar()

        expected = region.exists(url_bar_default_zoom_level_pattern.similar(0.92), 10)
        assert_true(self, expected, 'Zoom indicator not displayed by default in the url bar.')

        click_hamburger_menu_option('Customize...')

        expected = exists(zoom_controls_customize_page_pattern, 10)
        assert_true(self, expected, 'Zoom controls found in the \'Customize\' page.')

        drag_drop(zoom_controls_customize_page_pattern, toolbar_pattern, 0.5)
        time.sleep(Settings.UI_DELAY)
        reset_mouse()

        expected = exists(default_zoom_level_toolbar_customize_page_pattern, 10, in_region=Region(0, 0, SCREEN_WIDTH, 300))
        assert_true(self, expected, 'Zoom controls successfully dragged and dropped in toolbar.')

        close_customize_page()

        new_region = create_region_for_url_bar()

        expected = new_region.exists(default_zoom_level_toolbar_pattern, 10)
        assert_true(self, expected, 'Zoom controls still displayed in toolbar after the Customize page is closed.')

        expected = new_region.exists(url_bar_default_zoom_level_pattern.similar(0.92), 10)
        assert_true(self, expected, 'Zoom indicator not displayed in the url bar for default zoom level.')

        click(zoom_control_toolbar_decrease_pattern)

        expected = new_region.exists(zoom_control_90_pattern.similar(0.4), 10)
        assert_true(self, expected, 'Zoom controls are correctly displayed in toolbar after zoom level is decreased.')

        click(zoom_control_toolbar_increase_pattern)

        expected = new_region.exists(default_zoom_level_toolbar_pattern, 10)
        assert_true(self, expected, 'Zoom controls are correctly displayed in toolbar after zoom level is increased.')

        click(zoom_control_toolbar_increase_pattern)

        expected = new_region.exists(zoom_control_110_pattern, 10)
        assert_true(self, expected,
                    'Zoom controls are correctly displayed in toolbar after the second zoom level increase.')

        expected = new_region.exists(url_bar_default_zoom_level_pattern.similar(0.92), 10)
        assert_true(self, expected,
                    'Zoom indicator not displayed in the url bar after zoom control is activated in toolbar.')

        # Decrease the zoom indicator to 100% so that it won't be displayed in the url bar after zoom controls
        # deactivation.
        click(zoom_control_toolbar_decrease_pattern)

        expected = new_region.exists(default_zoom_level_toolbar_pattern, 10)
        assert_true(self, expected,
                    'Zoom controls are correctly displayed in toolbar after several zoom level increases/decreases.')

        remove_zoom_indicator_from_toolbar()

        expected = new_region.exists(url_bar_default_zoom_level_pattern.similar(0.92), 10)
        assert_true(self, expected,
                    'Zoom indicator not displayed in the url bar after zoom control is removed from toolbar.')

        new_reg = create_region_for_hamburger_menu()

        expected = new_reg.exists('100%', 10)
        assert_true(self, expected, 'By default zoom level is 100% in hamburger menu.')
