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
        dock_button = 'dock_to_side.png'
        dock_button_activated = 'dock_to_side_activated.png'
        separate_window_button = 'separate_window.png'
        menu = 'hamburger_menu.png'
        close_dev_tools_button = 'close_dev_tools.png'
        dev_tools_window = 'dev_tools_window.png'
        dock_message = 'dock_message.png'
        separate_window_message = 'separate_window_message.png'
        close_message = 'close_message.png'

        navigate(url)
        open_web_console()

        buttons = [dock_button, separate_window_button, close_dev_tools_button]
        button_messages = [dock_message, separate_window_message, close_message]

        for button in buttons:
            expected_buttons = exists(button, 5)
            assert_true(self, expected_buttons, 'Button %s has been found' % button)

        # Check if the labels are displayed when the cursor hovers over the buttons.

        for m_index, button in enumerate(buttons):
            hover(button)
            time.sleep(5)
            coord = find(button)
            button_region = Region(coord.x - 300, coord.y, 400, 100)
            expected_messages = button_region.exists(button_messages[m_index], 10)
            assert_true(self, expected_messages, 'Message %s found' % button_messages[m_index])

        # Checking the button functionality.
        coord = find(menu)
        right_upper_corner = Region(coord.x - 300, 0, 300, 300)

        click(dock_button)

        expected_1 = right_upper_corner.exists(dock_button_activated, 10)
        assert_true(self, expected_1, 'Dock to side button works.')

        click(separate_window_button)

        expected_2 = exists(dev_tools_window, 10)
        assert_true(self, expected_2, 'Show in separate window button works.')

        time.sleep(2)

        # Here is necessary to return back at the initial state in order to verify the close button functionality.
        click(dock_button_activated)

        time.sleep(1)

        click(close_dev_tools_button)
        try:
            expected_3 = waitVanish(dock_button_activated, 10)
            assert_true(self, expected_3, 'Close button works.')
        except Exception as error:
            logger.error('The Web Console can not be closed, aborting test.')
            raise error
