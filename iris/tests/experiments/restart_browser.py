# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.app = app
        self.meta = 'This is a test case that restarts the browser'

    def setup(self):
        """ Test case setup
        This overrides the setup method in the BaseTest class,
        so that it can use a profile that already has been launched.
        """
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        google_search_pattern = Pattern('google_search.png')
        amazon_pattern = Pattern('amazon.png')

        navigate('https://www.google.com/?hl=EN')
        expected_1 = exists(google_search_pattern, 10)
        assert_true(self, expected_1, 'Find Google search image')

        restart_firefox(self.app.fx_path, self.profile_path, url='https://www.amazon.com')
        expected_2 = exists(amazon_pattern, 10)
        assert_true(self, expected_2, 'Find Amazon image')

        return
