# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'Check that the \'Clear Recent History\' window is displayed properly.'

    def setup(self):
        """Test case setup

        This overrides the setup method in the BaseTest class, so that it can use a brand new profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.BRAND_NEW
        return

    def run(self):
        clear_recent_history_window = 'clear_recent_history_window.png'

        # Check that the Clear Recent History window is displayed properly.
        clear_recent_history()
        expected = exists(clear_recent_history_window, 10)
        assert_true(self, expected, 'Clear Recent History window was displayed properly.')
        type(Key.ESC)
