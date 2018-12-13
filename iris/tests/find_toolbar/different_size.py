# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Search on a window with a different size'
        self.test_case_id = '127247'
        self.test_suite_id = '2085'
        self.locales = ['en-US']

    def run(self):
        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_label_exists = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, 20)
        assert_true(self, soap_label_exists, 'The page is successfully loaded.')

        full_screen()

        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(FindToolbar.FINDBAR_TEXTBOX, 10)
        assert_true(self, find_toolbar_opened, 'Find Toolbar is opened.')

        paste('soap')
        click(FindToolbar.FIND_CASE_SENSITIVE)

        find_next()

        selected_label_exists = exists(LocalWeb.SOAP_WIKI_SOAP_ENVELOPE_LABEL_SELECTED, 5)
        unselected_label_exists = exists(LocalWeb.SOAP_WIKI_SOAP_XML_LABEL, 5)
        assert_true(self, selected_label_exists, 'The first one has a green background highlighted.')
        assert_true(self, unselected_label_exists, 'The others are not highlighted.')

        full_screen()

        selected_label_exists = exists(LocalWeb.SOAP_WIKI_SOAP_ENVELOPE_LABEL_SELECTED, 5)
        unselected_label_exists = exists(LocalWeb.SOAP_WIKI_SOAP_XML_LABEL, 5)
        assert_true(self, selected_label_exists, 'The first one has a green background highlighted.')
        assert_true(self, unselected_label_exists,
                    'The others are not highlighted.')
