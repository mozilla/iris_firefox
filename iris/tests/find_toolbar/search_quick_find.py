# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Search with the Quick Find [Failed due to bug (other items are not highlighted as pink)]'
        self.test_case_id = '127259'
        self.test_suite_id = '2085'
        self.locales = ['en-US']
        self.blocked_by = 'issue 1628'
        self.exclude = Platform.ALL

    def run(self):

        soap_label_pattern = Pattern('soap_label.png')
        see_label_selected_pattern = Pattern('cleaning_see_selected_label.png')
        quick_find_label_pattern = Pattern('quick_find_label.png')

        navigate(LocalWeb.WIKI_TEST_SITE)
        soap_label_exists = exists(soap_label_pattern, 20)
        assert_true(self, soap_label_exists, 'The page is successfully loaded.')

        type('/')
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(quick_find_label_pattern, 10)
        assert_true(self, find_toolbar_opened, 'Find Toolbar is opened.')

        type('see', interval=1)

        selected_label_exists = exists(see_label_selected_pattern, 5)
        assert_true(self, selected_label_exists, 'The first one has a green background highlighted.')
        assert_true(self, False,
                    'The others are not highlighted as pink')
