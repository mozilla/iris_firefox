# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='This is a test case that checks that Browser Control Console work as expected.',
        locale=['en-US'],
        test_case_id='120464',
        test_suite_id='1998'
    )
    def run(self, firefox):
        browser_console = Pattern('browser_console.png')
        clear_web_console = Pattern('clear.png')

        navigate('about:blank')
        pop_up_region = click_hamburger_menu_option('Web Developer')
        time.sleep(Settings.DEFAULT_UI_DELAY)

        pop_up_region.click('Browser Console')
        time.sleep(Settings.DEFAULT_UI_DELAY)
        assert exists(browser_console, 10), 'Browser Console successfully displayed.'
        assert exists(clear_web_console, 10), 'Clear the web console option is present.'

        click_window_control('close')
        try:
            assert wait_vanish(browser_console, 10), 'Browser Console successfully closed.'
        except FindError:
            raise FindError('Browser Console not closed')

        open_browser_console()
        click_window_control('minimize')
        try:
            assert wait_vanish(browser_console, 10), 'Browser Console successfully minimized.'
        except FindError:
            raise FindError('Browser Console not minimized.')

        restore_window_from_taskbar('browser_console')
        click_window_control('maximize')
        top_page = Screen.TOP_THIRD
        try:
            hover(clear_web_console)
            assert top_page.exists(browser_console, 10), 'Browser Console successfully maximized.'
        except FindError:
            raise FindError('Browser Console not maximized.')

        click_window_control('close')
