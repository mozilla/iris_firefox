# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Navigate back and forward on a page'
        self.test_case_id = '127261'
        self.test_suite_id = '2085'
        self.locales = ['en-US']

    def run(self):
        soap_label_pattern = LocalWeb.SOAP_WIKI_SOAP_LABEL

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_label_exists = exists(soap_label_pattern, 20)
        assert_true(self, soap_label_exists, 'The page is successfully loaded.')

        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_is_opened = exists(FindToolbar.FINDBAR_TEXTBOX, 15)
        assert_true(self, find_toolbar_is_opened, 'The find toolbar is opened')

        click(NavBar.BACK_BUTTON)

        find_toolbar_is_opened_previous_page = exists(FindToolbar.FINDBAR_TEXTBOX, 10)
        assert_true(self, find_toolbar_is_opened_previous_page, 'The find toolbar is present on the previous page')

        click(NavBar.FORWARD_BUTTON)

        find_toolbar_is_opened_next_page = exists(FindToolbar.FINDBAR_TEXTBOX, 10)
        assert_true(self, find_toolbar_is_opened_next_page, 'The find toolbar is present on the next page')
