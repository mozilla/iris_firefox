from test_case import *


class test(base_test):
    def __init__(self, app):
        base_test.__init__(self, app)
        self.meta = "This is a test for adding a website in the bookmarks section"

    def run(self):
        url = "www.amazon.com"

        navigate(url)

        if exists("amazon.png", 2):

            # Add bookmark with keyboard shortcut
            bookmark_page()

            # Sometimes we need to wait a bit for favicon to be loaded
            time.sleep(3)
            press("enter")

            # Sometimes we need to wait because UI is animating after
            # bookmark was created and library icon image isn't found
            time.sleep(3)

            # Look for new bookmark via library menu button
            click("library.png")
            press("down")

            if exists("amazon_bookmark_1.png", 5):
                print ("PASS")
            else:
                print ("FAIL")

            # We need to close the library menu before next test
            press("escape")

            # Sometimes we need to wait a bit for favicon to be loaded
            time.sleep(3)

            # Look for bookmark in bookmark menu
            bookmarks_sidebar()
            time.sleep(1)
            typewrite("amazon")
            if exists("amazon_bookmark_2.png", 5):
                print ("PASS")
            else:
                print ("FAIL")

        else:
            print ("FAIL")
