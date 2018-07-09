# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that checks if the Bookmarks Toolbar can be enabled from the Bookmarks Menu.'

    def run(self):
        view_bookmarks_toolbar = 'view_bookmarks_toolbar.png'
        toolbar_enabled = 'toolbar_is_active.png'

        navigate('about:blank')

        access_bookmarking_tools(view_bookmarks_toolbar)

        enabled_toolbar_assert = exists(toolbar_enabled, 10)
        assert_true(self, enabled_toolbar_assert, 'Bookmarks Toolbar has been activated.')
