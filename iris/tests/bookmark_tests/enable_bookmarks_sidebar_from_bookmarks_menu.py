# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that checks if the Bookmarks Sidebar can be enabled from the Bookmarks Menu.'
        self.test_case_id = '4091'
        self.test_suite_id = '75'

    def run(self):
        view_bookmarks_sidebar = 'view_bookmarks_sidebar.png'
        sidebar_enabled = 'sidebar_is_active.png'

        navigate('about:blank')

        access_bookmarking_tools(view_bookmarks_sidebar)

        enabled_sidebar_assert = exists(sidebar_enabled, 10)
        assert_true(self, enabled_sidebar_assert, 'Bookmarks Sidebar has been enabled from the Bookmarks Menu.')
