# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import datetime

from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test of sending messages on Yahoo web messenger'
        self.exclude = Platform.ALL

    def run(self):
        yahoo_login = 'yahoo_login.png'
        yahoo_messenger_conversation_button = 'yahoo_messenger_conversation_button.png'
        write_message_field = 'write_message_field.png'
        yahoo_messenger_test_message = 'yahoo_messenger_test_message.png'
        delete_button = 'delete_button.png'
        unsend_button = 'unsend_button.png'


        url = 'https://login.yahoo.com/?.done=https%3A%2F%2Fmessenger.yahoo.com%2F&.pd=c%3DU4ZyUvq72e4_yB0G1IX7c9q7dSw-&.src=messenger&.lang=en'
        today = datetime.now()

        # Open the login page.
        navigate(url)
        time.sleep(3)
        expected_1 = exists(yahoo_login, 10)
        assert_true(self, expected_1, 'Login page loaded successfully')
        time.sleep(3)

        # Fill in the credentials and login.
        username = get_credential('Yahoo', 'username')
        password = get_credential('Yahoo', 'password')
        paste(username)
        type(Key.ENTER)
        time.sleep(3)
        paste(password)
        type(Key.ENTER)
        time.sleep(3)

        # Don't save the credentials in Firefox.
        dont_save_password()

        expected_2 = exists(yahoo_messenger_conversation_button, 10)
        assert_true(self, expected_2, 'The conversation button is displayed successfully')
        # Start a new conversation.
        click(yahoo_messenger_conversation_button)
        # Add the recipient.
        type('test1')
        # Add the message.
        click(write_message_field)
        type('test2 ' + str(today))
        # Send the message.
        type(Key.ENTER)
        # Delete the previously sent message.
        expected_3 = exists(yahoo_messenger_test_message, 10)
        assert_true(self, expected_3, 'Sent message is displayed properly')
        hover(yahoo_messenger_test_message)
        click(delete_button)
        time.sleep(1)
        click(unsend_button)
        try:
            expected_4 = waitVanish(yahoo_messenger_test_message, 10)
            assert_true(self, expected_4, 'Sent message is deleted successfully')
        except:
            raise FindError('Sent message is not deleted')