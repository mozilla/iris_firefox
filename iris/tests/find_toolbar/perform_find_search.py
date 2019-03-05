# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Perform a search'
        self.test_case_id = '127239'
        self.test_suite_id = '2085'
        self.locales = ['en-US']

    def run(self):
        soap_label_pattern = LocalWeb.SOAP_WIKI_SOAP_LABEL
        from_wikipedia_label_pattern = Pattern('from_wikipedia_label.png')

        # Open Firefox and navigate to a popular website
        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)
        soap_label_exists = exists(soap_label_pattern, 20)
        assert_true(self, soap_label_exists, 'The page is successfully loaded.')

        # Open the Find toolbar
        open_find()
        edit_select_all()
        edit_delete()
        find_toolbar_opened = exists(FindToolbar.FINDBAR_TEXTBOX, 10)
        assert_true(self, find_toolbar_opened, 'Find Toolbar is opened.')

        # Enter a search term and press ENTER
        paste('From Wikipedia')
        type(Key.ENTER)
        selected_label_exists = exists(from_wikipedia_label_pattern.similar(0.6), DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, selected_label_exists, 'All the matching words/characters are found.')
