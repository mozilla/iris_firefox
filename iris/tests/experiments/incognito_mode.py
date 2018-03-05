from test_case import *

from sikuli import *


class test(base_test):
    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "This is a test for checking the incognito navigation"


    def run(self):
        url = "https://www.google.com/?hl=EN"
        #check if incognito mode works

        new_incognito_window()

        pattern = "incognito.png"
        if exists(pattern, 10):
            result = "PASS"
        else:
            result = "FAIL"

        print result

        #check basic_url in incognito mode
        navigate(url)

        pattern_navigation = "google_search.png"

        if exists(pattern_navigation, 10):
            result_nav = "PASS"
        else:
            result_nav = "FAIL"

        print result_nav