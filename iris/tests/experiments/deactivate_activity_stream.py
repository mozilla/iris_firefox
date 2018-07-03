# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This tests the ability to activate/deactivate the activity stream'
        self.fx_version = '>=62'

    def run(self):
        preference = 'browser.newtabpage.activity-stream.feeds.topsites'
        change_preference(preference, 'false')
        new_tab()
        new_tab()

        # Verify that activity stream has been disabled
        screen_text = get_firefox_region().text()
        logger.debug('Found text: %s' % screen_text)
        expected_1 = 'TOP SITES' in screen_text
        assert_false(self, expected_1, 'Find TOP SITES')

        change_preference(preference, 'true')
        new_tab()
        new_tab()

        # Verify that activity stream has been enabled

        # NOTE: sometimes fails due to poor text recognition
        # e.g. "TOP SITES" is seen as "TOP srres" on at least one Linux config
        # TODO: make more robust

        screen_text = get_firefox_region().text()
        expected_1 = 'TOP SITES' in screen_text
        logger.debug('Found text: %s' % screen_text)
        assert_true(self, expected_1, 'Find TOP SITES')
