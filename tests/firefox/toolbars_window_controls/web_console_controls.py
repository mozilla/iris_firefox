# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='This is a test case that checks if the Web Console controls work as expected.',
        locale=['en-US'],
        test_case_id='120137',
        test_suite_id='1998'
    )
    def run(self, firefox):
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

        navigate('about:home')
        open_web_console()

        buttons = [responsive_design_button_pattern, customize_dev_tools_pattern, close_dev_tools_button_pattern]
        button_messages = [responsive_design_message_pattern,
                           customize_dev_tools_message_pattern,
                           close_message_pattern]

        right_upper_corner = Region(Screen.SCREEN_WIDTH / 2, 0, Screen.SCREEN_WIDTH / 2, Screen.SCREEN_HEIGHT / 2)
        left_upper_corner = Region(0, 0, Screen.SCREEN_WIDTH / 2, Screen.SCREEN_HEIGHT / 2)
        button_region = Region(Screen.SCREEN_WIDTH / 2, Screen.SCREEN_HEIGHT / 2, Screen.SCREEN_WIDTH / 2,
                               Screen.SCREEN_HEIGHT / 2)

        for button in buttons:
            assert button_region.exists(button, 5), 'Option {} has been found.'.format(button)

        for m_index, button in enumerate(buttons):
            button_region.hover(button)
            assert button_region.exists(
                button_messages[m_index], 10), 'Message {} found.'.format(button_messages[m_index])

        button_region.click(responsive_design_button_pattern)
        assert exists(responsive_design_active_pattern, 10), 'Responsive Design Mode is enabled.'

        button_region.click(customize_dev_tools_pattern)
        try:
            wait(dock_to_left_pattern, 10)
            logger.debug('Dock to left option found.')
            click(dock_to_left_pattern)
        except FindError:
            raise FindError('Dock to left option not found, aborting.')
        assert left_upper_corner.exists(customize_dev_tools_pattern, 10), 'Dock to left option works as expected.'

        left_upper_corner.click(customize_dev_tools_pattern)
        try:
            wait(dock_to_right_pattern, 10)
            logger.debug('Dock to right option found.')
            click(dock_to_right_pattern)
        except FindError:
            raise FindError('Dock to right option not found, aborting.')
        assert right_upper_corner.exists(customize_dev_tools_pattern, 10), 'Dock to right option works as expected.'

        right_upper_corner.click(customize_dev_tools_pattern)
        try:
            wait(separate_window_pattern, 10)
            logger.debug('Separate Window option found.')
            click(separate_window_pattern)
        except FindError:
            raise FindError('Separate Window option not found, aborting.')
        assert exists(dev_tools_window_pattern, 10), 'Separate Window option works as expected.'

        click(customize_dev_tools_pattern)
        try:
            wait(dock_to_bottom_pattern, 10)
            logger.debug('Dock To Bottom option found.')
            click(dock_to_bottom_pattern)
        except FindError:
            raise FindError('Dock To Bottom option not found, aborting.')
        assert exists(close_dev_tools_button_pattern, 10), 'Dock To Bottom option works as expected.'

        button_region.click(close_dev_tools_button_pattern)
        try:
            assert button_region.wait_vanish(customize_dev_tools_pattern, 10), 'Close button works.'
        except FindError:
            raise FindError('The Web Console can not be closed, aborting test.')
