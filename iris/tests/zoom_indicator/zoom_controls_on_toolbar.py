# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that checks the zoom controls functionality on toolbar.'

    def run(self):
        url = 'about:home'
        search_bar = 'search_bar.png'
        hamburger_menu = 'hamburger_menu.png'
        zoom_controls_customize_page = 'zoom_controls_customize_page.png'
        toolbar = 'toolbar.png'
        default_zoom_level_toolbar_customize_page = 'default_zoom_level_toolbar_customize_page.png'
        default_zoom_level_toolbar = 'default_zoom_level_toolbar.png'
        zoom_control_toolbar_decrease = 'zoom_control_toolbar_decrease.png'
        zoom_control_toolbar_increase = 'zoom_control_toolbar_increase.png'
        zoom_control_90 = 'zoom_control_90.png'
        zoom_control_110 = 'zoom_control_110.png'
        hamburger_menu_zoom_indicator = 'hamburger_menu_zoom_indicator.png'

        navigate(url)

        expected = exists(hamburger_menu, 10)
        assert_true(self, expected, 'Page successfully loaded, hamburger menu found.')

        region = create_region_for_url_bar()

        expected = region.exists(search_bar, 10)
        assert_true(self, expected, 'Zoom level not displayed by default in the url bar.')

        click_hamburger_menu_option('Customize...')
        time.sleep(1)

        # Searching for text 'Drag'
        expected = exists('Drag', 10, in_region=Region(0, 0, 800, 300))
        assert_true(self, expected, '\'Customize\' page present.')

        expected = exists(zoom_controls_customize_page, 10, in_region=Region(0, 0, 900, 300))
        assert_true(self, expected, 'Zoom controls found in the \'Customize\' page.')

        dragDrop(zoom_controls_customize_page, toolbar, 0.5)
        time.sleep(1)

        expected = exists(default_zoom_level_toolbar_customize_page, 10, in_region=Region(0, 0, SCREEN_WIDTH, 300))
        assert_true(self, expected, 'Zoom controls successfully dragged and dropped in the toolbar.')

        close_customize_page()
        time.sleep(1)

        expected = exists(default_zoom_level_toolbar, 10, in_region=Region(0, 0, SCREEN_WIDTH, 300))
        assert_true(self, expected, 'Zoom controls still displayed in the toolbar after the Customize page is closed.')

        click(zoom_control_toolbar_decrease)

        expected = exists(zoom_control_90, 10, in_region=Region(0, 0, SCREEN_WIDTH, 300))
        assert_true(self, expected, 'Zoom controls are correctly displayed in the toolbar after decrease.')

        click(zoom_control_toolbar_increase)

        expected = exists(default_zoom_level_toolbar, 10, in_region=Region(0, 0, SCREEN_WIDTH, 300))
        assert_true(self, expected, 'Zoom controls are correctly displayed in the toolbar after increase.')

        click(zoom_control_toolbar_increase)

        expected = exists(zoom_control_110, 10, in_region=Region(0, 0, SCREEN_WIDTH, 300))
        assert_true(self, expected, 'Zoom controls are correctly displayed in the toolbar after the second increase.')

        expected = exists(search_bar, 10)
        assert_true(self, expected,
                    'Zoom level not displayed in the url bar after zoom control is activated in the toolbar.')

        # Decrease the zoom level to 100% so that it won't be displayed in the url bar after deactivation.
        click(zoom_control_toolbar_decrease)

        expected = exists(default_zoom_level_toolbar, 10, in_region=Region(0, 0, SCREEN_WIDTH, 300))
        assert_true(self, expected,
                    'Zoom controls are correctly displayed in the toolbar after several zoom level increase/decrease.')

        remove_zoom_indicator_from_toolbar()
        time.sleep(1)

        expected = exists(search_bar, 10)
        assert_true(self, expected,
                    'Zoom level not displayed in the url bar after zoom control is removed from the toolbar.')

        new_region = create_region_for_hamburger_menu()

        expected = new_region.exists(hamburger_menu_zoom_indicator, 10)
        assert_true(self, expected, 'Zoom level is 100% by default.')
