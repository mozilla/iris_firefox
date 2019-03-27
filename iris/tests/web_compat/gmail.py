# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Web compatibility test for gmail.com'
        self.enabled = False

    def run(self):
        url = 'mail.google.com'
        compose_pattern = Pattern('compose_email.png')
        receiver = 'ionut'
        subject = 'Gmail Test'
        message = 'test'
        inbox_pattern = Pattern('gmail_inbox.png')
        email_pattern = Pattern('email_present.png')
        delete_email_pattern = Pattern('delete_email.png')

        navigate(url)

        time.sleep(5)

        self.login_gmail()
        logger.info('Successful login')
        time.sleep(5)
        type(Key.ESC)

        expected_1 = exists(compose_pattern, 10)
        assert_true(self, expected_1, 'Compose button is present on the page.')

        click(compose_pattern)
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

        expected_2 = exists(inbox_pattern, 10)
        assert_true(self, expected_2, 'Gmail Inbox has been accessed successfully.')

        click(inbox_pattern)
        time.sleep(1)

        expected_3 = exists(email_pattern, 10)
        assert_true(self, expected_3, 'Email is received successfully.')

        click(email_pattern)
        logger.debug('Email has been accessed.')
        time.sleep(1)
        click(delete_email_pattern)
        time.sleep(2)
        logger.debug('Email has been erased.')
        type(Key.ENTER)

    def login_gmail(self):
        username = get_config_property('Gmail', 'username')
        password = get_config_property('Gmail', 'password')
        login = Pattern('login_gmail.png')

        expected_login = exists(login, 10)
        assert_true(self, expected_login, 'Login fields are present.')

        type(username)
        for i in range(3):
            type(Key.TAB)
        type(Key.ENTER)
        time.sleep(2)
        type(password)
        type(Key.TAB)
        type(Key.ENTER)
