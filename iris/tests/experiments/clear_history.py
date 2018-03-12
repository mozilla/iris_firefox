from test_case import *

from sikuli import *


class test(base_test):
    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "This is a test for clearing browser history"


    def run(self):

        url = "https://www.amazon.com"
        amazon_history = "amazon_history.png"

        navigate(url)
        wait ("amazon.png", 10)
        clear_recent_history()
        time.sleep(2)
        type(Key.ENTER)
        time.sleep(2)
        click ("home.png")
        history_sidebar()
        time.sleep(2)
        type ("amazon")

        if exists(amazon_history, 5):
            print "FAIL"
        else:
            print "PASS"
