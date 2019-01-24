# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = "Test for new restore Firefox focus test"

    def run(self):
        navigate('https://github.com/mozilla/iris/pull/1923')
        time.sleep(15)
        restore_firefox_focus()
        time.sleep(5)
