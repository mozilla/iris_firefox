# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This is a test case that checks if the Web Console controls work as expected.'
        self.test_case_id = '120137'
        self.test_suite_id = '1998'
        self.locales = ['en-US']

    def run(self):

        close_dev_tools_button_pattern = Pattern('close_dev_tools.png')
        dev_tools_window_pattern = Pattern('dev_tools_window.png')
        close_message_pattern = Pattern('close_message.png')
        responsive_design_button_pattern = Pattern('responsive_design.png')
        customize_dev_tools_pattern = Pattern('customize_developer_tools.png')
        customize_dev_tools_message_pattern = Pattern('customize_dev_tools_message.png')
        responsive_design_message_pattern = Pattern('responsive_design_message.png')
        responsive_design_active_pattern = Pattern('responsive_design_active.png')
        dock_to_left_pattern = Pattern('dock_to_left.png')
        dock_to_right_pattern = Pattern('dock_to_right.png')
        separate_window_pattern = Pattern('separate_window_option.png')
        dock_to_bottom_pattern = Pattern('dock_to_bottom_option.png')

        open_web_console()

        right_upper_corner = Region(SCREEN_WIDTH / 2, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        left_upper_corner = Region(0, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        button_region = Region(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        responsive_design_button_displayed = exists(responsive_design_button_pattern)
        assert_true(self, responsive_design_button_displayed, '"Responsive design" button displayed')

        hover(responsive_design_button_pattern)

        responsive_design_message_displayed = exists(responsive_design_message_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, responsive_design_message_displayed, '"Responsive design" message is displayed')

        customize_dev_tools_button_displayed = exists(customize_dev_tools_pattern)
        assert_true(self, customize_dev_tools_button_displayed, '"Customize dev tools" button displayed')

        hover(customize_dev_tools_pattern)

        customize_dev_tools_message_displayed = exists(customize_dev_tools_message_pattern)
        assert_true(self, customize_dev_tools_message_displayed, '"Customize dev tools" message is displayed')

        close_dev_tools_button_displayed = exists(close_dev_tools_button_pattern, in_region=button_region)
        assert_true(self, close_dev_tools_button_displayed, '"Close dev tools" button displayed')

        hover(close_dev_tools_button_pattern, in_region=button_region)

        close_message_displayed = exists(close_message_pattern)
        assert_true(self, close_message_displayed, '"Close dev tools" message is displayed')

        click(responsive_design_button_pattern)

        responsive_design_assert = exists(responsive_design_active_pattern)
        assert_true(self, responsive_design_assert, 'Responsive Design Mode is enabled.')

        customize_button_in_bottom = exists(customize_dev_tools_pattern, in_region=button_region)
        assert_true(self, customize_button_in_bottom, '"Customize dev tools" button is located in window\'s bottom')

        click(customize_dev_tools_pattern, in_region=button_region)

        dock_to_left_button_exists = exists(dock_to_left_pattern)
        assert_true(self, dock_to_left_button_exists, '"Dock to Left" button is displayed')

        click(dock_to_left_pattern)

        dock_to_left_works = exists(customize_dev_tools_pattern, in_region=left_upper_corner)
        assert_true(self, dock_to_left_works, '"Dock to Left" option works as expected.')

        click(customize_dev_tools_pattern, in_region=left_upper_corner)

        dock_to_right_button_displayed = exists(dock_to_right_pattern)
        assert_true(self, dock_to_right_button_displayed, '"Dock to Right" button is displayed')

        click(dock_to_right_pattern)

        docked_to_right = exists(customize_dev_tools_pattern, in_region=right_upper_corner)
        assert_true(self, docked_to_right, 'Panel wad docked to right')

        click(customize_dev_tools_pattern, in_region=right_upper_corner)

        separate_window_button_displayed = exists(separate_window_pattern)
        assert_true(self, separate_window_button_displayed, '"Separate window" button is displayed')

        click(separate_window_pattern)

        separate_window_opened = exists(dev_tools_window_pattern)
        assert_true(self, separate_window_opened, '"Separate Window" option works as expected.')

        separate_window_location = find(dev_tools_window_pattern)

        separate_window_region = Region(separate_window_location.x, separate_window_location.y,
                                        SCREEN_WIDTH - separate_window_location.x, SCREEN_HEIGHT // 2)

        customize_button_in_separate_window = exists(customize_dev_tools_pattern, in_region=separate_window_region)
        assert_true(self, customize_button_in_separate_window, '"Customize dev tools" button is inside separate window')

        click(customize_dev_tools_pattern, in_region=separate_window_region)

        dock_to_bottom_button_displayed = exists(dock_to_bottom_pattern)
        assert_true(self, dock_to_bottom_button_displayed, '"Dock to Bottom" button is displayed')

        click(dock_to_bottom_pattern)

        dock_to_bottom_assert = exists(close_dev_tools_button_pattern)
        assert_true(self, dock_to_bottom_assert, 'Dock To Bottom option works as expected.')

        click(close_dev_tools_button_pattern, in_region=button_region)

        try:
            customize_button_disappeared = wait_vanish(customize_dev_tools_pattern, in_region=button_region)
            assert_true(self, customize_button_disappeared, 'Close button works.')
        except FindError:
            raise FindError('The Web Console can not be closed, aborting test.')
