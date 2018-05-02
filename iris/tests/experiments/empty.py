# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is an empty test case that does nothing'
        self.assets = BaseTest.set_asset_path(self, os.path.split(__file__)[0])

    def run(self):
        """
        This is where your test logic goes.
        """
        navigate (self.assets + "empty.html")
        time.sleep(5)
        assert_equal(self, 1, 1, 'test')
        assert_true(self, False, 'test')
        return
