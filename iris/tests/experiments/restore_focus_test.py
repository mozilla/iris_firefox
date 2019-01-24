# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This is a test to check if restore_firefox_focus works after adjustment'

    def run(self):
        navigate('https://bugzilla.mozilla.org/show_bug.cgi?id=1520224')
        time.sleep(15)
        restore_firefox_focus()