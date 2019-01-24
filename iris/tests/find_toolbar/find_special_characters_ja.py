# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *
import sys


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Search a word that contains special characters (2)'
        self.test_case_id = '127276'
        self.test_suite_id = '2085'
        self.locales = ['en-US']

    def run(self):
        first_japan_highlighted_pattern = Pattern('first_japan_highlighted.png')
        second_japan_highlighted_pattern = Pattern('second_japan_highlighted.png')
        japan_not_highlighted_pattern = Pattern('japan_not_highlighted.png')

        test_page_local = self.get_asset_path('ja.htm')
        navigate(test_page_local)

        page_loaded_anchor_exists = exists(LocalWeb.SOAP_WIKI_TEST_LABEL_PATTERN, 20)
        assert_true(self, page_loaded_anchor_exists, 'The page is successfully loaded.')

        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(FindToolbar.FINDBAR_TEXTBOX, 10)
        assert_true(self, find_toolbar_opened, 'Find Toolbar is opened.')

        reload(sys)
        sys.setdefaultencoding('utf8')

        paste('辻希美')

        selected_label_exists = exists(first_japan_highlighted_pattern, 1)
        not_selected_label_exists = exists(japan_not_highlighted_pattern, 1)
        assert_true(self, selected_label_exists, 'The first one has a green background highlighted.')
        assert_true(self, not_selected_label_exists, 'The second one is not highlighted.')

        find_next()

        second_highlighted_exists = exists(second_japan_highlighted_pattern, 1)
        assert_true(self, second_highlighted_exists, 'The green box is moved with the current item.')

        sys.setdefaultencoding('ascii')
