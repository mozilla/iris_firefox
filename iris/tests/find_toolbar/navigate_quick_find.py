# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Navigate through Quick Find items [Failed due to absence of pink highlight]'
        self.test_case_id = '127260'
        self.test_suite_id = '2085'
        self.locales = ['en-US']
        self.blocked_by = {'id': 'issue_1628', 'platform': Platform.ALL}

    def run(self):
        navigate(LocalWeb.WIKI_TEST_SITE)

        soap_label_exists = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, 20)
        assert_true(self, soap_label_exists, 'The page is successfully loaded.')

        type('/')
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(FindToolbar.QUICK_FIND_LABEL, 10)
        assert_true(self, find_toolbar_opened, 'Find Toolbar is opened.')

        type('see', interval=1)

        selected_label_exists = exists(LocalWeb.SOAP_WIKI_CLEANING_SEE_SELECTED_LABEL, 5)

        type(Key.F3)

        changed_selection_exists = exists(LocalWeb.SOAP_WIKI_SEE_LABEL)
        assert_true(self, selected_label_exists, 'The first one has a green background highlighted.')
        assert_true(self, changed_selection_exists, 'The green box is moved on next.')
        assert_true(self, False,
                    'The others are not highlighted as pink [known issue]')
