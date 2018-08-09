# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'Websites can be bookmarked via keyboard shortcut.'
        self.test_case_id = '4088'
        self.test_suite_id = '75'

    def run(self):
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        mozilla_page_assert = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, mozilla_page_assert, 'Mozilla page loaded successfully.')

        bookmark_page()

        page_bookmarked_assert = exists('page_bookmarked.png', 10)
        assert_true(self, page_bookmarked_assert, 'The page was successfully bookmarked via keyboard shortcut.')
