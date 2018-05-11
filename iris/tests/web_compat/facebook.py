# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'Web compability test for facebook.com'
        self.exclude = Platform.ALL

    def run(self):
        url = 'www.facebook.com'
        news_feed = 'news_feed.png'
        message_area = 'type_message.png'
        post_message = 'post_message.png'
        post = 'post.png'
        delete_post = 'delete_post.png'

        navigate(url)

        time.sleep(3)

        self.login_facebook()
        logger.debug('Successful login')
        time.sleep(3)
        type(Key.ESC)
        time.sleep(4)
        type(Key.ESC)

        # Post message

        expected_1 = exists(news_feed, 10)
        assert_true(self, expected_1, 'News Feed has been accessed')

        if Settings.getOS() == Platform.MAC:
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
            click(message_area)
            time.sleep(2)
            type('test')
            click(post_message)
            time.sleep(3)

        expected_2 = exists(post, 10)
        assert_true(self, expected_2, 'Message has been posted successfully')

        # Delete post

        if Settings.getOS() == Platform.MAC:
            for i in range(7):
                type(Key.TAB)
            time.sleep(2)
            type(Key.ESC)
            time.sleep(2)
            type(Key.ENTER)
            time.sleep(2)
            click(delete_post)
            time.sleep(3)
            for i in range(2):
                type(Key.TAB)
            time.sleep(2)
            type(Key.ENTER)
            time.sleep(3)
        else:
            click(message_area)
            time.sleep(1)
            type(Key.ESC)
            time.sleep(1)
            type(Key.ENTER)
            time.sleep(2)
            click(delete_post)
            time.sleep(2)
            for i in range(5):
                type(Key.TAB)
            time.sleep(2)
            type(Key.ENTER)
            time.sleep(2)

        try:
            expected_3 = waitVanish(post, 10)
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
        username = get_credential('Facebook', 'username')
        password = get_credential('Facebook', 'password')
        login = 'login_check.png'

        expected_login = exists(login, 10)
        assert_true(self, expected_login, 'LogIn fields are present')

        type(username)
        type(Key.TAB)
        type(password)
        type(Key.TAB)
        type(Key.ENTER)
