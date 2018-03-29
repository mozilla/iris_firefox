# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *



class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "Web compability test for facebook.com--Login"
        self.enable = False




    def run(self):
        url="www.facebook.com"

        navigate(url)

        time.sleep(5)

        #login - please see the login_facebook method in general.py

        self.login_facebook()
        logger.info("Successful login")
        time.sleep(3)
        type(Key.ESC)
        time.sleep(4)
        type(Key.ESC)


        #post message


        if exists("news_feed.png", 10):
            if get_os() == "osx":
                for i in range(7):
                    type(Key.TAB)
                time.sleep(2)

                type("test")
                for i in range(3):
                    type(Key.TAB)

                time.sleep(2)
                type(Key.ENTER)
                logger.info("Message has been posted successfully")
                time.sleep(5)
            else:
                click("type_message.png")
                time.sleep(2)
                type("test")
                click("post_message.png")
                time.sleep(2)
        else:
            logger.error("Post Failed...")

        #delete post

        if exists("post.png", 10):
            if get_os() == "osx":
                for i in range(7):
                    type(Key.TAB)
                time.sleep(2)
                type(Key.ESC)
                time.sleep(2)
                type(Key.ENTER)
                time.sleep(2)
                click("delete_post.png")
                time.sleep(3)
                for i in range(2):
                    type(Key.TAB)
                time.sleep(2)
                type(Key.ENTER)
                time.sleep(3)
                logger.info("The message has been deleted")
            else:
                click("type_message.png")
                time.sleep(1)
                type(Key.ESC)
                time.sleep(1)
                type(Key.ENTER)
                time.sleep(2)
                click("delete_post.png")
                time.sleep(2)
                for i in range(5):
                    type(Key.TAB)
                time.sleep(2)
                type(Key.ENTER)
                time.sleep(2)

        else:
            logger.info("No message posted")

        time.sleep(5)

        #scroll down and up

        for i in range(15):
            scroll_down()
        time.sleep(2)
        for i in range(15):
            scroll_up()
        time.sleep(2)


    def login_facebook(self):
        username = get_credential("Facebook","username")
        password = get_credential("Facebook","password")
        if exists("login_check.png", 10):
            type(username)
            type(Key.TAB)
            type(password)
            type(Key.TAB)
            type(Key.ENTER)
        else:
            logger.error("Facebook page was not loaded...")





