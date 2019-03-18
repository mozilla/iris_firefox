# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This is a test of creating various Firefox instances with arguments'

        # Disabling test. Due to our new profile handling, it will be hard to support the
        # use case of multiple Fx instances, such as this test.
        self.enabled = False

    def run(self):
        amazon_pattern = Pattern('amazon.png')

        time.sleep(5)
        args = ['-width', '800', '-height', '800', '-new-tab', 'http://www.mozilla.org']
        launch_firefox(path=self.browser.path, profile=Profile.DEFAULT, args=args)

        time.sleep(5)
        args = ['-width', '600', '-height', '600', '-search', 'firefox']
        launch_firefox(path=self.browser.path, profile=Profile.DEFAULT, args=args)

        time.sleep(5)
        args = ['-width', '400', '-height', '400', '-private-window', 'http://amazon.com']
        launch_firefox(path=self.browser.path, profile=Profile.DEFAULT, args=args)

        expected_1 = exists(amazon_pattern, 20)

        quit_firefox()
        time.sleep(5)
        quit_firefox()
        time.sleep(5)
        quit_firefox()
        time.sleep(5)

        assert_true(self, expected_1, 'Found amazon image')
