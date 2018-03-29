# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *



class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "Web compability test for gmail.com--Login"
        self.enable = False


    def run(self):
        url = "mail.google.com"
        compose = "compose_email.png"
        receiver = "ionut"
        subject = "Gmail Test"
        message = "test"
        inbox = "gmail_inbox.png"
        email = "email_present.png"
        delete_email = "delete_email.png"

        navigate(url)

        time.sleep(5)

        self.login_gmail()
        logger.info("Successful Log IN ")
        time.sleep(5)
        type(Key.ESC)

        if exists(compose, 10):
            click(compose)
            time.sleep(2)
            type(receiver)
            time.sleep(2)
            type(Key.ENTER)
            time.sleep(1)
            type(Key.TAB)
            time.sleep(1)
            type(subject)
            time.sleep(2)
            type(Key.TAB)
            time.sleep(2)
            type(message)
            time.sleep(2)
            type(Key.TAB)
            type(Key.ENTER)
            logger.debug("Email has been sent...")
            time.sleep(2)

        if exists(inbox, 10):
            click(inbox)
            time.sleep(1)
            if exists(email, 10):
                click(email)
                logger.debug("Email has been accessed..")
                time.sleep(1)
                click(delete_email)
                time.sleep(2)
                logger.debug("Email has been erased..")
                type(Key.ENTER)
            else:
                print "FAIL"
        else:
            logger.error("Page was not loaded")


    def login_gmail(self):
        username = get_credential("Gmail", "username")
        password = get_credential("Gmail", "password")
        if exists("login_gmail.png", 10):
            type(username)
            for i in range(3):
                type(Key.TAB)
            type(Key.ENTER)
            time.sleep(2)
            type(password)
            type(Key.TAB)
            type(Key.ENTER)
        else:
            logger.error("Gmail Log In PAge was not loaded..")
