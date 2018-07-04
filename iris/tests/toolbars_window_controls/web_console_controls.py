# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that checks if the Web Console controls work as expected'

    def run(self):

        url = 'about:home'
        close_dev_tools_button = 'close_dev_tools.png'
        dev_tools_window = 'dev_tools_window.png'
        close_message = 'close_message.png'
        responsive_design_button = 'responsive_design.png'
        customize_dev_tools = 'customize_developer_tools.png'
        customize_dev_tools_message = 'customize_dev_tools_message.png'
        responsive_design_message = 'responsive_design_message.png'
        responsive_design_active = 'responsive_design_active.png'
        dock_to_side = 'dock_to_side_option.png'
        separate_window = 'separate_window_option.png'
        dock_to_bottom = 'dock_to_bottom_option.png'

        navigate(url)
        open_web_console()

        buttons = [responsive_design_button, customize_dev_tools, close_dev_tools_button]
        button_messages = [responsive_design_message, customize_dev_tools_message, close_message]

        screen = get_screen()
        right_upper_corner = Region(screen.getW() / 2, screen.getY(), screen.getW() / 2, screen.getH() / 2)
        button_region = Region(right_upper_corner.getBottomLeft().getX(), right_upper_corner.getBottomLeft().getY(),
                               screen.getW() / 2, screen.getH() / 2)

        for button in buttons:
            expected_buttons = button_region.exists(button, 5)
            assert_true(self, expected_buttons, 'option %s has been found' % button)

        # Check if the labels are displayed when the cursor hovers over the options.

        for m_index, button in enumerate(buttons):
            button_region.hover(button)
            expected_messages = button_region.exists(button_messages[m_index], 10)
            assert_true(self, expected_messages, 'Message %s found' % button_messages[m_index])

        # Checking the button functionality.

        button_region.click(responsive_design_button)

        responsive_design_assert = exists(responsive_design_active, 10)
        assert_true(self, responsive_design_assert, 'Responsive Design Mode is enabled.')

        button_region.click(customize_dev_tools)

        try:
            wait(dock_to_side, 10)
            logger.debug('Dock to side option found.')
            click(dock_to_side)
        except FindError:
            logger.error('Dock to side option not found, aborting.')
            raise FindError

        dock_to_side_assert = right_upper_corner.exists(customize_dev_tools, 10)
        assert_true(self, dock_to_side_assert, 'Dock to side option works as expected.')

        right_upper_corner.click(customize_dev_tools)

        try:
            wait(separate_window, 10)
            logger.debug('Separate Window option found.')
            click(separate_window)
        except FindError:
            logger.error('Separate Window option not found, aborting.')
            raise FindError

        separate_window_assert = exists(dev_tools_window, 10)
        assert_true(self, separate_window_assert, 'Separate Window option works as expected.')

        click(customize_dev_tools)

        try:
            wait(dock_to_bottom, 10)
            logger.debug('Dock To Bottom option found.')
            click(dock_to_bottom)
        except FindError:
            logger.error('Dock To Bottom option not found, aborting.')
            raise FindError

        dock_to_bottom_assert = exists(close_dev_tools_button, 10)
        assert_true(self, dock_to_bottom_assert, 'Dock To Bottom option works as expected')

        button_region.click(close_dev_tools_button)

        try:
            close_button_assert = button_region.waitVanish(customize_dev_tools, 10)
            assert_true(self, close_button_assert, 'Close button works.')
        except FindError:
            logger.error('The Web Console can not be closed, aborting test.')
            raise FindError
