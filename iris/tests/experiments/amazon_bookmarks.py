from test_case import *


class test(base_test):
    def __init__(self, app):
        base_test.__init__(self, app)
        self.meta = "This is a test for adding a website in the bookmarks section"

    def run(self):
        url = "www.amazon.com"
        amazon_image = "amazon.png"
        amazon_bookmark_image_1 = "amazon_bookmark_1.png"
        amazon_bookmark_image_2 = "amazon_bookmark_2.png"

        navigate(url)

        expected_1 = exists(amazon_image, 0.5)
        assert_true(self, expected_1, 'Find amazon image')

        bookmark_page()

        # Sometimes we need to wait a bit for favicon to be loaded
        time.sleep(3)
        type(Key.ENTER)

        # Sometimes we need to wait because UI is animating after
        # bookmark was created and library icon image isn't found
        time.sleep(3)

        # Look for new bookmark via library menu button
        click("library.png")
        type(Key.TAB)
        type(Key.ENTER)
        time.sleep(1)

        expected_2 = exists(amazon_bookmark_image_1, 0.5)
        assert_true(self, expected_2, 'Find amazon bookmark 1 image')

        type(Key.ESC)

        # Sometimes we need to wait a bit for favicon to be loaded
        time.sleep(3)

        # Look for bookmark in bookmark menu
        bookmarks_sidebar()
        time.sleep(1)
        type("amazon")
        time.sleep(1)

        expected_3 = exists(amazon_bookmark_image_2, 0.5)
        assert_true(self, expected_3, 'Find amazon bookmark 2 image')
