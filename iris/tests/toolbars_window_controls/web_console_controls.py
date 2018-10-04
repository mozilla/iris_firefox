# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that checks if the Web Console controls work as expected.'
        self.test_case_id = '120137'
        self.test_suite_id = '1998'
        self.locales = ['en-US']

    def run(self):

        url = 'about:home'
        close_dev_tools_button_pattern = Pattern('close_dev_tools.png')
        dev_tools_window_pattern = Pattern('dev_tools_window.png')
        close_message_pattern = Pattern('close_message.png').similar(0.5)
        responsive_design_button_pattern = Pattern('responsive_design.png')
        customize_dev_tools_pattern = Pattern('customize_developer_tools.png')
        customize_dev_tools_message_pattern = Pattern('customize_dev_tools_message.png').similar(0.5)
        responsive_design_message_pattern = Pattern('responsive_design_message.png').similar(0.5)
        responsive_design_active_pattern = Pattern('responsive_design_active.png').similar(0.4)
        dock_to_left_pattern = Pattern('dock_to_left.png')
        dock_to_right_pattern = Pattern('dock_to_right.png')
        separate_window_pattern = Pattern('separate_window_option.png')
        dock_to_bottom_pattern = Pattern('dock_to_bottom_option.png').similar(0.5)

        navigate(url)
        open_web_console()

        buttons = [responsive_design_button_pattern, customize_dev_tools_pattern, close_dev_tools_button_pattern]
        button_messages = [responsive_design_message_pattern,
                           customize_dev_tools_message_pattern,
                           close_message_pattern]

        right_upper_corner = Region(SCREEN_WIDTH / 2, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        left_upper_corner = Region(0, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        button_region = Region(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        for button in buttons:
            expected_buttons = button_region.exists(button, 5)
            assert_true(self, expected_buttons, 'option %s has been found.' % button)

        # Check if the labels are displayed when the cursor hovers over the options.

        for m_index, button in enumerate(buttons):
            button_region.hover(button)
            expected_messages = button_region.exists(button_messages[m_index], 10)
            assert_true(self, expected_messages, 'Message %s found.' % button_messages[m_index])

        # Checking the button functionality.

        button_region.click(responsive_design_button_pattern)

        responsive_design_assert = exists(responsive_design_active_pattern, 10)
        assert_true(self, responsive_design_assert, 'Responsive Design Mode is enabled.')

        button_region.click(customize_dev_tools_pattern)

        try:
            wait(dock_to_left_pattern, 10)
            logger.debug('Dock to left option found.')
            click(dock_to_left_pattern)
        except FindError:
            raise FindError('Dock to left option not found, aborting.')

        dock_to_left_assert = left_upper_corner.exists(customize_dev_tools_pattern, 10)
        assert_true(self, dock_to_left_assert, 'Dock to left option works as expected.')

        left_upper_corner.click(customize_dev_tools_pattern)

        try:
            wait(dock_to_right_pattern, 10)
            logger.debug('Dock to right option found.')
            click(dock_to_right_pattern)
        except FindError:
            raise FindError('Dock to right option not found, aborting.')

        dock_to_right_assert = right_upper_corner.exists(customize_dev_tools_pattern, 10)
        assert_true(self, dock_to_right_assert, 'Dock to right option works as expected.')

        right_upper_corner.click(customize_dev_tools_pattern)

        try:
            wait(separate_window_pattern, 10)
            logger.debug('Separate Window option found.')
            click(separate_window_pattern)
        except FindError:
            raise FindError('Separate Window option not found, aborting.')

        separate_window_assert = exists(dev_tools_window_pattern, 10)
        assert_true(self, separate_window_assert, 'Separate Window option works as expected.')

        click(customize_dev_tools_pattern)

        try:
            wait(dock_to_bottom_pattern, 10)
            logger.debug('Dock To Bottom option found.')
            click(dock_to_bottom_pattern)
        except FindError:
            raise FindError('Dock To Bottom option not found, aborting.')

        dock_to_bottom_assert = exists(close_dev_tools_button_pattern, 10)
        assert_true(self, dock_to_bottom_assert, 'Dock To Bottom option works as expected.')

        button_region.click(close_dev_tools_button_pattern)

        try:
            close_button_assert = button_region.wait_vanish(customize_dev_tools_pattern, 10)
            assert_true(self, close_button_assert, 'Close button works.')
        except FindError:
            raise FindError('The Web Console can not be closed, aborting test.')
