# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that checks the zoom indicator + window state when using the mouse wheel.'
        self.test_case_id = '7454'
        self.test_suite_id = '242'
        self.locales = ['en-US']

    def run(self):
        url = LocalWeb.FIREFOX_TEST_SITE
        url_bar_default_zoom_level_pattern = Pattern('url_bar_default_zoom_level.png')
        url_bar_110_zoom_level_pattern = Pattern('url_bar_110_zoom_level.png')
        url_bar_300_zoom_level_pattern = Pattern('url_bar_300_zoom_level.png')
        hamburger_menu_pattern = NavBar.HAMBURGER_MENU

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        region = create_region_for_url_bar()
        click(LocalWeb.FIREFOX_LOGO)

        expected = region.exists(url_bar_default_zoom_level_pattern, 10)
        assert_true(self, expected, 'Zoom indicator not displayed by default in the url bar.')

        zoom_with_mouse_wheel(1, ZoomType.IN)

        new_region = create_region_for_url_bar()

        click(hamburger_menu_pattern.target_offset(-170, 15))

        expected = new_region.exists(url_bar_110_zoom_level_pattern, 10)
        assert_true(self, expected, 'Zoom level successfully increased, zoom indicator found in the url bar.')

        zoom_with_mouse_wheel(19, ZoomType.IN)

        expected = new_region.exists(url_bar_300_zoom_level_pattern, 10)
        assert_true(self, expected, 'Zoom level successfully increased, maximum zoom level(300%) reached.')

        if Settings.get_os() == Platform.WINDOWS or Settings.get_os() == Platform.LINUX:
            minimize_window()
            minimize_window()
        else:
            minimize_window()

        try:
            expected = wait_vanish(LocalWeb.FIREFOX_LOGO, 10)
            assert_true(self, expected, 'Window successfully minimized.')
        except FindError:
            raise FindError('Window not minimized.')

        restore_window_from_taskbar()

        if Settings.get_os() == Platform.WINDOWS or Settings.get_os() == Platform.LINUX:
            maximize_window()

        expected = exists(hamburger_menu_pattern, 10)
        assert_true(self, expected, 'Window successfully opened again.')

        expected = new_region.exists(url_bar_300_zoom_level_pattern, 10)
        assert_true(self, expected, 'Zoom indicator still display 300%.')
