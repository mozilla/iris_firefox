from test_case import *

from sikuli import *


class test(base_test):
    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "This is a test for clearing browser history"


    def run(self):

        url = "https://www.google.com/?hl=EN"
        history = "history.png"
        clear_history = "clear_history.png"
        clear_button = "clear_button.png"
        library = "library.png"
        access_history = "access_history"

        navigate(url)

        open_history_menu()

        if exists(history, 10):
            click(library)
            wait(access_history, 10)
            click(access_history)
            wait(clear_history, 10)
            click(clear_history)
            wait(clear_button, 10)
            click(clear_button)

            time.sleep(1)

            if exists(history, 10):
                print "FAIL"
            else:
                print "PASS"

        else:
            print "Browser history has been cleared already"





