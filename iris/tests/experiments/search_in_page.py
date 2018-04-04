from test_case import *


class test(base_test):
    def __init__(self, app):
        base_test.__init__(self, app)
        self.meta = "This is a test for text search in page"

    def run(self):
        url = "https://www.google.com/?hl=EN"
        google_search_image = "google_search.png"
        search_in_page_image = "search_in_page.png"

        navigate(url)

        expected_1 = wait(google_search_image)
        assert_true(self, expected_1, 'Wait for google search image to appear')

        open_find()
        type("Gmail")

        expected_2 = exists(search_in_page_image, 0.5)
        assert_true(self, expected_2, 'Find search in page image')
