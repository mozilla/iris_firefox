# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Search for an inexistent String on the page'
        self.test_case_id = '127245'
        self.test_suite_id = '2085'
        self.locales = ['en-US']

    def run(self):
        soap_label_pattern = LocalWeb.SOAP_WIKI_SOAP_LABEL
        phrase_not_found_label_pattern = FindToolbar.FIND_STATUS_PHRASE_NOT_FOUND
        merge_red_textbox_pattern = Pattern('merge_red_textbox.png')

        # Open Firefox and navigate to a popular website
        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_label_exists = exists(soap_label_pattern, 20)
        assert_true(self, soap_label_exists, 'The page is successfully loaded.')

        # Open the Find Toolbar
        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(FindToolbar.FINDBAR_TEXTBOX, 10)
        assert_true(self, find_toolbar_opened, 'Find Toolbar is opened.')

        # Search for an inexistent String on the page
        type('merge', interval=1)

        red_textbox_exists = exists(merge_red_textbox_pattern, 5)
        assert_true(self, red_textbox_exists, 'Input field has a red background')

        label_not_found = exists(phrase_not_found_label_pattern, 5)
        assert_true(self, label_not_found, 'Phrase not found appears')

        # Tap the "Find next", "Find previous" arrows from the toolbar.
        click(FindToolbar.FIND_NEXT)
        click(FindToolbar.FIND_PREVIOUS)

        red_textbox_exists = exists(merge_red_textbox_pattern, 5)
        assert_true(self, red_textbox_exists, 'The arrows do not change the state.')
