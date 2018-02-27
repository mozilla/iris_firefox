from test_case import *
from sikuli import *


class test(base_test):
    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "This is a test for adding an website in the bookmarks section"

    def run(self):
        url = "www.amazon.com"

        navigate(url)

        if exists("amazon.png", 10):

            wait("bookmarks.png", 10)
            click("bookmarks.png")

            if exists("bookmark_menu.png", 10):

                wait("bookmark_menu.png", 10)
                click("bookmark_menu.png")
                # adding bookmark with keyboard shortcut

                add_bookmark()
                time.sleep(6)
                open_bookmark_menu()

                if exists("check_bookmark.png", 10):
                    print "PASS"
                else:
                    print "FAIL"

            else:
                "FAIL"

        else:
            "FAIL"
