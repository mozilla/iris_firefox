from test_case import *


class test(base_test):
    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "This is a test for adding a website in the bookmarks section"

    def run(self):
        url = "www.amazon.com"

        navigate(url)

        if exists("amazon.png", 10):

            # Add bookmark with keyboard shortcut
            add_bookmark()

            # Look for new bookmark via library menu button
            click("library.png")
            type(Key.DOWN)
            type(Key.ENTER)

            if exists("amazon_bookmark.png", 10):
                print "PASS"
            else:
                print "FAIL"

            # Look for bookmark in bookmark menu
            open_bookmark_menu()
            type("amazon")
            if exists("amazon_bookmark.png", 10):
                print "PASS"
            else:
                print "FAIL"

        else:
            print "FAIL"
