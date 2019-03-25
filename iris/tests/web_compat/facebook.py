# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Web compatibility test for facebook.com'
        self.enabled = False

    def run(self):
        url = 'www.facebook.com'
        news_feed_pattern = Pattern('news_feed.png')
        message_area_pattern = Pattern('type_message.png')
        post_message_pattern = Pattern('post_message.png')
        post_pattern = Pattern('post.png')
        delete_post_pattern = Pattern('delete_post.png')

        navigate(url)

        time.sleep(3)

        self.login_facebook()
        logger.debug('Successful login')
        time.sleep(3)
        type(Key.ESC)
        time.sleep(4)
        type(Key.ESC)

        # Post message

        expected_1 = exists(news_feed_pattern, 10)
        assert_true(self, expected_1, 'News Feed has been accessed')

        if Settings.get_os() == Platform.MAC:
            for i in range(7):
                type(Key.TAB)
            time.sleep(2)
            type('test')
            for i in range(3):
                type(Key.TAB)
            time.sleep(2)
            type(Key.ENTER)
            time.sleep(3)
        else:
            click(message_area_pattern)
            time.sleep(2)
            type('test')
            click(post_message_pattern)
            time.sleep(3)

        expected_2 = exists(post_pattern, 10)
        assert_true(self, expected_2, 'Message has been posted successfully')

        # Delete post

        if Settings.get_os() == Platform.MAC:
            for i in range(7):
                type(Key.TAB)
            time.sleep(2)
            type(Key.ESC)
            time.sleep(2)
            type(Key.ENTER)
            time.sleep(2)
            click(delete_post_pattern)
            time.sleep(3)
            for i in range(2):
                type(Key.TAB)
            time.sleep(2)
            type(Key.ENTER)
            time.sleep(3)
        else:
            click(message_area_pattern)
            time.sleep(1)
            type(Key.ESC)
            time.sleep(1)
            type(Key.ENTER)
            time.sleep(2)
            click(delete_post_pattern)
            time.sleep(2)
            for i in range(5):
                type(Key.TAB)
            time.sleep(2)
            type(Key.ENTER)
            time.sleep(2)

        try:
            expected_3 = wait_vanish(post_pattern, 10)
            assert_true(self, expected_3, 'The message has been deleted')
        except Exception as error:
            logger.error('The message can not be deleted')
            raise error

        time.sleep(5)

        # Scroll down and up

        for i in range(15):
            scroll_down()

        time.sleep(2)

        for i in range(15):
            scroll_up()

        time.sleep(2)

    def login_facebook(self):
        username = get_config_property('Facebook', 'username')
        password = get_config_property('Facebook', 'password')
        login = Pattern('login_check.png')

        expected_login = exists(login, 10)
        assert_true(self, expected_login, 'LogIn fields are present')

        type(username)
        type(Key.TAB)
        type(password)
        type(Key.TAB)
        type(Key.ENTER)
