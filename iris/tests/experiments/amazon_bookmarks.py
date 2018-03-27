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
            bookmark_page()

            # Sometimes we need to wait a bit for favicon to be loaded
            time.sleep(3)
            type(Key.ENTER)

            # Sometimes we need to wait because UI is animating after
            # bookmark was created and library icon image isn't found
            time.sleep(5)

            # Look for new bookmark via library menu button
            click("library.png")
            time.sleep(1)
            type(Key.DOWN)
            type(Key.ENTER)

            if exists("amazon_bookmark_1.png", 5):
                print "PASS"
            else:
                print "FAIL"

            # We need to close the library menu before next test
            type(Key.ESC)

            # Sometimes we need to wait a bit for favicon to be loaded
            time.sleep(3)

            # Look for bookmark in bookmark menu
            bookmarks_sidebar()
            time.sleep(1)
            type("amazon")
            if exists("amazon_bookmark_2.png", 5):
                print "PASS"
            else:
                print "FAIL"

        else:
            print "FAIL"
