# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This tests the ability to activate/deactivate the activity stream.'
        self.fx_version = '>=62'
        self.enabled = False

    def run(self):
        top_sites_pattern = Pattern('top_sites.png')

        preference = 'browser.newtabpage.activity-stream.feeds.topsites'
        change_preference(preference, 'false')
        new_tab()

        # Verify that activity stream has been disabled.
        expected_2 = exists(top_sites_pattern, 10)
        assert_false(self, expected_2, 'Find TOP SITES.')

        change_preference(preference, 'true')
        new_tab()

        # Verify that activity stream has been enabled.
        expected_3 = exists(top_sites_pattern, 10)
        assert_true(self, expected_3, 'Find TOP SITES.')
