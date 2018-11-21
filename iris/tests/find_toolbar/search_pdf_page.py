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

        find_toolbar_pattern = Pattern('find_toolbar_text.png')
        pdf_logo_pattern = Pattern('pdf_page_logo.png')
        pdf_logo_pattern.similarity = 0.6
        first_printer_hl_pattern = Pattern('first_printer_highlight.png')
        second_printer_hl_pattern = Pattern('second_printer_highlight.png')
        second_printer_white_pattern = Pattern('second_printer_white.png')

        test_page_local = self.get_asset_path('pdf.pdf')
        navigate(test_page_local)

        navigated_to_pdf_url = exists(pdf_logo_pattern, 80)

        assert_true(self, navigated_to_pdf_url, 'PDF URL loaded successfully.')

        open_find()

        # Remove all text from the Find Toolbar

        edit_select_all()
        edit_delete()

        find_toolbar_is_opened = exists(find_toolbar_pattern, 5)

        assert_true(self, find_toolbar_is_opened, 'The Find Toolbar is successfully displayed '
                                                  'by pressing CTRL + F / Cmd + F,.')

        type('printer')
        type(Key.ENTER)

        word_printer_hl_exists = exists(first_printer_hl_pattern, 5)
        word_printer_white_exists = exists(second_printer_white_pattern, 5)

        assert_true(self, (word_printer_hl_exists and word_printer_white_exists),
                    'All the matching words / characters are found.')

        first_occurrence_highlighted = exists(first_printer_hl_pattern, 5)

        assert_true(self, first_occurrence_highlighted, 'First occurrence highlighted')

        # Switch to next occurrence
        find_next()

        second_occurrence_highlighted = exists(second_printer_hl_pattern, 5)

        assert_true(self, second_occurrence_highlighted, 'Second occurrence highlighted')

        # Get back to first occurrence
        find_previous()

        before_scroll_first_exists = exists(first_printer_hl_pattern, 5)

        for i in range(4):
            scroll_down()

        for i in range(4):
            scroll_up()

        after_scroll_first_exists = exists(first_printer_hl_pattern, 5)

        assert_true(self, before_scroll_first_exists and after_scroll_first_exists,
                    'Occurrence exists after scroll up and down. No checkboarding is present')

