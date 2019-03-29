# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import random
from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Web compatibility test for linkedin.com'
        self.enabled = False

    def run(self):
        url = 'www.linkedin.com'
        linkedin_login_page_pattern = Pattern('linkedin_login_page.png')
        linkedin_email_field_pattern = Pattern('linkedin_email_field.png')
        linkedin_home_page_pattern = Pattern('linkedin_home_page.png')
        linkedin_post_button_pattern = Pattern('linkedin_post_button.png')
        linkedin_message_is_posted_pattern = Pattern('linkedin_message_is_posted.png')
        linkedin_menu_pattern = Pattern('linkedin_menu.png')
        linkedin_sign_out_pattern = Pattern('linkedin_sign_out.png')

        navigate(url)

        expected_1 = exists(linkedin_login_page_pattern, 10)
        assert_true(self, expected_1, 'The page is successfully loaded.')

        expected_2 = exists(linkedin_email_field_pattern, 10)
        assert_true(self, expected_2, 'The email field successfully found.')

        click(linkedin_email_field_pattern)
        login_site("Linkedin")
        dont_save_password()

        expected_3 = exists(linkedin_home_page_pattern, 10)
        assert_true(self, expected_3, 'User successfully logged in.')

        click(linkedin_post_button_pattern, 0)
        time.sleep(2)
        # Posting a message with a random character at the end. Same message cannot be posted twice, an error is thrown.
        paste("This is a test message " + random.choice('abcdefghijklmnopqrstuvwxyz'))
        click(linkedin_post_button_pattern)

        expected_4 = exists(linkedin_message_is_posted_pattern, 10)
        assert_true(self, expected_4, 'Message successfully posted.')

        # Scroll down.
        for number in range(30):
            scroll_down()

        time.sleep(2)

        # Scroll up.
        for number in range(30):
            scroll_up()

        click(linkedin_menu_pattern)
        time.sleep(0.5)
        click(linkedin_sign_out_pattern)

        expected_5 = exists(linkedin_login_page_pattern, 10)
        assert_true(self, expected_5, 'User successfully logged out.')
