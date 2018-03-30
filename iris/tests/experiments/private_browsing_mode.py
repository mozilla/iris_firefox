from test_case import *


class test(base_test):
    def __init__(self, app):
        base_test.__init__(self, app)
        self.meta = "This is a test for checking private browsing navigation"

    def run(self):
        url = "https://www.google.com/?hl=EN"
        # check if incognito mode works

        new_private_window()

        pattern = "private_browsing.png"
        if exists(pattern, 10):
            result = "PASS"
        else:
            result = "FAIL"

        print result

        # check basic_url in incognito mode
        navigate(url)

        pattern_navigation = "google_search.png"

        if exists(pattern_navigation, 10):
            result_nav = "PASS"
        else:
            result_nav = "FAIL"

        print result_nav
