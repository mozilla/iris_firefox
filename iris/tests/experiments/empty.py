# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This is an empty test case that does nothing'
        self.tags = 'broken,test,sanity,123'
        self.enabled = False

    def run(self):
        """
        This is where your test logic goes.
        """
        assert_equal(self, 1, 1, 'test')
        assert_true(self, False, 'test')
        return
