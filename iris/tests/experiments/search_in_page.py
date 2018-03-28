from test_case import *


class test(base_test):
    def __init__(self, app):
        base_test.__init__(self, app)
        self.meta = "This is a test for text search in page"

    def run(self):

        url = "https://www.google.com/?hl=EN"
        pattern = "search_in_page.png"
        navigate(url)

        try:
            wait("google_search.png", 10)
        except:
            logger.error("Can't find Google image in page, aborting test")
            return

        open_find()
        type("Gmail")

        if exists(pattern, 5):
            result = "PASS"
        else:
            result = "FAIL"

        print result
