# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'Web compability test for gmail.com--Login'

    def run(self):
        url = 'mail.google.com'
        compose = 'compose_email.png'
        receiver = 'ionut'
        subject = 'Gmail Test'
        message = 'test'
        inbox = 'gmail_inbox.png'
        email = 'email_present.png'
        delete_email = 'delete_email.png'

        navigate(url)

        time.sleep(5)

        self.login_gmail()
        logger.info('Successful Log IN ')
        time.sleep(5)
        type(Key.ESC)

        expected_1 = exists(compose, 10)
        assert_true(self, expected_1, 'Compose button is present on the page!')

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
        logger.debug('Email has been sent...')
        time.sleep(2)

        expected_2 = exists(inbox, 10)
        assert_true(self, expected_2, 'Gmail Inbox has been accessed successfully!')

        click(inbox)
        time.sleep(1)

        expected_3 = exists(email, 10)
        assert_true(self, expected_3, 'Email is received successfully!')

        click(email)
        logger.debug('Email has been accessed..')
        time.sleep(1)
        click(delete_email)
        time.sleep(2)
        logger.debug('Email has been erased..')
        type(Key.ENTER)

    def login_gmail(self):
        username = get_credential('Gmail', 'username')
        password = get_credential('Gmail', 'password')
        login = 'login_gmail.png'

        expected_login = exists(login, 10)
        assert_true(self, expected_login, 'LogIn fields are present!')

        type(username)
        for i in range(3):
            type(Key.TAB)
        type(Key.ENTER)
        time.sleep(2)
        type(password)
        type(Key.TAB)
        type(Key.ENTER)
