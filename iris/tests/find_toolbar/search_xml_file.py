# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Search on a XML page'
        self.test_case_id = '127272'
        self.test_suite_id = '2085'
        self.locales = ['en-US']

    def run(self):
        xml_page_logo_pattern = Pattern('xml_page_logo.png')
        first_occurrence_highlighted_pattern = Pattern('xml_text_first_occurrence_pattern.png')
        second_occurrence_highlighted_pattern = Pattern('xml_text_second_occurrence_pattern.png').similar(0.6)

        # Open Firefox and open a [XML page]
        test_page_local = self.get_asset_path('cd_catalog.xml')
        navigate(test_page_local)

        xml_url_logo_exists = exists(xml_page_logo_pattern, 5)
        assert_true(self, xml_url_logo_exists, 'The page is successfully loaded.')

        # Open the Find Toolbar
        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_is_opened = exists(FindToolbar.FINDBAR_TEXTBOX, 5)
        assert_true(self, find_toolbar_is_opened, 'The Find Toolbar is successfully displayed ')

        # Search for a term that appears on the page
        type('for')

        text_first_occurrence_exists = exists(first_occurrence_highlighted_pattern, 5)
        assert_true(self, text_first_occurrence_exists, 'The first occurrence is highlighted.')

        # Navigate through found items
        find_next()

        text_second_occurrence_exists = exists(second_occurrence_highlighted_pattern, 5)
        assert_true(self, text_second_occurrence_exists, 'The second occurrence is highlighted.')

        # Scroll the page up and down
        find_previous()

        text_first_occurrence_exists = exists(first_occurrence_highlighted_pattern, 5)
        assert_true(self, text_first_occurrence_exists, 'The first occurrence is highlighted before scrolling.')

        repeat_key_down(4)
        repeat_key_up(4)

        text_first_occurrence_exists_after_scroll = exists(first_occurrence_highlighted_pattern, 5)
        assert_true(self, text_first_occurrence_exists_after_scroll,
                    'The first occurrence is highlighted after scrolling.')
