# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='Browser controls work as expected.',
        locale=['en-US'],
        test_case_id='119481',
        test_suite_id='1998'
    )
    def run(self, firefox):
        window_controls_minimize_pattern = Pattern('window_controls_minimize.png')
        hover_minimize_control_pattern = Pattern('hover_minimize_control.png')
        window_controls_restore_pattern = Pattern('window_controls_restore.png')
        hover_restore_control_pattern = Pattern('hover_restore_control.png')
        window_controls_maximize_pattern = Pattern('window_controls_maximize.png')
        hover_maximize_control_pattern = Pattern('hover_maximize_control.png')
        window_controls_close_pattern = Pattern('window_controls_close.png')
        hover_close_control_pattern = Pattern('hover_close_control.png')

        navigate(LocalWeb.FIREFOX_TEST_SITE)
        assert exists(LocalWeb.FIREFOX_LOGO, 10), 'Page successfully loaded, firefox logo found.'

        if OSHelper.is_linux():
            Mouse().move(Location(0, 0))

        hover(window_controls_minimize_pattern)
        assert exists(hover_minimize_control_pattern, 10), 'Hover over the \'minimize\' button works correctly.'

        if OSHelper.is_windows() or OSHelper.is_linux():
            hover(window_controls_restore_pattern)
            assert exists(hover_restore_control_pattern, 10), 'Hover over the \'restore\' button works correctly.'

        if OSHelper.is_mac():
            middle = find(hover_maximize_control_pattern)
            Mouse().move(Location(middle.x + 7, middle.y + 5))
            assert exists(hover_maximize_control_pattern, 10), 'Hover over the \'maximize\' button works correctly.'

            Mouse().move(Location(middle.x - 35, middle.y + 5))
            assert exists(hover_close_control_pattern.similar(0.7), 10), \
                'Hover over the \'close\' button works correctly.'
        else:
            hover(window_controls_close_pattern)
            assert exists(hover_close_control_pattern, 10), 'Hover over the \'close\' button works correctly.'

        if OSHelper.is_windows() or OSHelper.is_linux():
            click_window_control('restore', 'main')
            time.sleep(Settings.DEFAULT_UI_DELAY)
            hover(window_controls_maximize_pattern)
            assert exists(hover_maximize_control_pattern, 10), \
                'Hover over the \'maximize\' button works correctly; Window successfully restored.'
        if OSHelper:
            hover(Pattern('home_button.png'))
        click_window_control('minimize', 'main')
        time.sleep(Settings.DEFAULT_UI_DELAY)

        try:
            assert wait_vanish(LocalWeb.FIREFOX_LOGO, 10), 'Window successfully minimized.'
        except FindError:
            raise FindError('Window not minimized.')

        restore_window_from_taskbar()

        if OSHelper.is_windows():
            click_window_control('maximize', 'main')

        assert exists(LocalWeb.FIREFOX_LOGO, 10), 'Window successfully opened again.'

        click_window_control('close', 'main')

        try:
            assert wait_vanish(LocalWeb.FIREFOX_LOGO, 10), 'Window successfully closed.'
        except FindError:
            assert False, 'Window successfully closed.'
