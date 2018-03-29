# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *
from datetime import datetime



class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "This is a test of sending messages on Yahoo web messenger"


    def run(self):
        url = "https://login.yahoo.com/?.done=https%3A%2F%2Fmessenger.yahoo.com%2F&.pd=c%3DU4ZyUvq72e4_yB0G1IX7c9q7dSw-&.src=messenger&.lang=en"
        today = datetime.now()
        # Open the login page.
        navigate(url)

        if exists("yahoo_login.png", 10):
            # Fill in the credentials and login.
            username = get_credential("Yahoo", "username")
            password = get_credential("Yahoo", "password")
            paste(username)
            type(Key.ENTER)
            time.sleep(3)
            paste(password)
            type(Key.ENTER)

            # Don't save the credentials in Firefox.
            dont_save_password()

            if exists("yahoo_messenger_conversation_button.png", 10):
                # Start a new conversation.
                click("yahoo_messenger_conversation_button.png")
                # Add the recipient.
                type("test1")
                # Add the message.
                click("write_message_field.png")
                type("test2 "+str(today))
                # Send the message.
                type(Key.ENTER)
                # Delete the previously sent message.
                if exists("yahoo_messenger_test_message.png", 10):
                    hover("yahoo_messenger_test_message.png")
                    click("delete_button.png")
                    click("unsend_button.png")
                    waitVanish("yahoo_messenger_test_message.png", 10)
                    result = "PASS"
                else:
                    result = "FAIL"
            else:
                result = "FAIL"
        else:
            result = "FAIL"

        print result
