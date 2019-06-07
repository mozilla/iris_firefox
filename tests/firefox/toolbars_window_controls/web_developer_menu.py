# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='This is a test case that checks that Developer Toolbar controls work as expected.',
        locale=['en-US'],
        test_case_id='119483',
        test_suite_id='1998',
        exclude=OSPlatform.ALL
    )
    def run(self, firefox):

        navigate("about:home")
        open_web_developer_menu()
        left_corner_region = Region(0, Screen.SCREEN_HEIGHT / 2, Screen.SCREEN_WIDTH / 2, Screen.SCREEN_HEIGHT / 2)
        right_corner_region = Region(Screen.SCREEN_WIDTH / 2, Screen.SCREEN_HEIGHT / 2, Screen.SCREEN_WIDTH / 2,
                                     Screen.SCREEN_HEIGHT / 2)

        web_developer_text_assert = Screen().exists(Pattern('web_developer_insert.png'), 10)
        assert web_developer_text_assert, 'Web developer bar is present.'
        if OSHelper.is_mac():
            left_corner_region.click(Pattern('web_developer_close_button.png'))
            logger.debug('Closing web developer bar.')
        else:
            right_corner_region.click(Pattern('web_developer_close_button.png'))
            logger.debug('Closing web developer bar.')
        if OSHelper.is_mac():
            try:
                close_button_assert = left_corner_region.wait_vanish(Pattern('web_developer_close_button.png'), 5)
                assert close_button_assert, 'Bar was closed.'
            except FindError:
                raise FindError('Bar was NOT closed.')

            open_web_developer_menu()
            time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
            paste('console open')
            type(Key.ENTER)
            console_items = ['Inspector', 'Debugger', 'Console', 'Performance', 'Memory']
            resize_region = Region(left_corner_region.x, left_corner_region.y - 100,
                                   left_corner_region.width, left_corner_region.height)
            for word in console_items:
                assert resize_region.exists(word), 'Item is present: \'{}\''.format(word)

        else:
            try:
                dev_close_button_assert = right_corner_region.wait_vanish(Pattern('web_developer_close_button.png'), 4)
                assert dev_close_button_assert, 'Web developer bar was closed.'
            except FindError:
                raise FindError('Web developer bar was NOT closed.')

            open_web_developer_menu()
            time.sleep(Settings.UI_DELAY_LONG)
            paste('console open')
            type(Key.ENTER)
            logger.debug('Opening console from command line.')
            console_items = ['Inspector', 'Debugger', 'Console', 'Performance', 'Memory', 'Network', 'Storage']
            for word in console_items:
                assert left_corner_region.exists(word), 'Item is present: \'{}\''.format(word)
