# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Search on a PDF page'
        self.test_case_id = '127271'
        self.test_suite_id = '2085'
        self.locales = ['en-US']

    def run(self):
        pdf_logo_pattern = Pattern('pdf_page_logo.png').similar(0.6)
        first_occurrence_highlighted_pattern = Pattern('first_printer_highlight.png')
        second_occurrence_highlighted_pattern = Pattern('second_printer_highlight.png')
        second_occurrence_unhighlighted_pattern = Pattern('second_printer_white.png')

        # Open Firefox and open a [PDF page]
        test_page_local = self.get_asset_path('pdf.pdf')
        navigate(test_page_local)
        navigated_to_pdf_url = exists(pdf_logo_pattern, 80)
        assert_true(self, navigated_to_pdf_url, 'PDF URL loaded successfully.')

        # Open the Find Toolbar
        open_find()
        edit_select_all()
        edit_delete()
        find_toolbar_is_opened = exists(FindToolbar.FINDBAR_TEXTBOX, 5)
        assert_true(self, find_toolbar_is_opened, 'The Find Toolbar is successfully displayed')

        # Search for a term that appears on the page
        type('printer')
        type(Key.ENTER)
        first_occurrence_highlighted = exists(first_occurrence_highlighted_pattern, 5)
        assert_true(self, first_occurrence_highlighted, 'The first occurrence is highlighted')
        second_occurrence_unhighlighted = exists(second_occurrence_unhighlighted_pattern, 5)
        assert_true(self, second_occurrence_unhighlighted, 'The second occurrence is not highlighted')

        # Navigate through found items
        find_next()
        second_occurrence_highlighted = exists(second_occurrence_highlighted_pattern, 5)
        assert_true(self, second_occurrence_highlighted, 'The second occurrence is highlighted')

        # Scroll the page up and down
        find_previous()
        first_occurrence_before_scrolling_highlighted = exists(first_occurrence_highlighted_pattern, 5)
        assert_true(self, first_occurrence_before_scrolling_highlighted,
                    'The first occurrence is highlighted before scrolling')

        repeat_key_down(4)
        repeat_key_up(4)
        first_occurrence_after_scrolling_highlighted = exists(first_occurrence_highlighted_pattern, 5)
        assert_true(self, first_occurrence_after_scrolling_highlighted,
                    'The first occurrence is highlighted after scrolling')
