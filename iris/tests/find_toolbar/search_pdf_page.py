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
        """
        Search on a PDF page

        STEP 1:
            DESCRIPTION:
                Open Firefox and open a [PDF page](http://www.pdf995.com/samples/pdf.pdf)

            EXPECTED:
                PDF page is loaded.

        STEP 2:
            DESCRIPTION:
                Open the Find Toolbar (CTRL+F).

            EXPECTED:
                Find Toolbar is opened.

        STEP 3:
            DESCRIPTION:
                Search for a term that appears on the page.

            EXPECTED:
                All the matching words/characters are found. The first one has a green background highlighted, and the others are not highlighted.

        STEP 4:
            DESCRIPTION:
                Navigate through found items (F3, SHIFT+F3)

            EXPECTED:
                The green box is moved with the current item.

        STEP 5:
            DESCRIPTION:
                Scroll the page up and down.

            EXPECTED:
                No checkboarding is present. The performance is good.

        NOTES:
            Initial version - Pavel Ciapa  - 11-Nov-2018
            Code review complete - Paul Prokhorov - 16-Nov-2018
        """

        find_toolbar_pattern = Pattern('find_toolbar_text.png')
        pdf_logo_pattern = Pattern('pdf_page_logo.png')
        pdf_logo_pattern.similarity = 0.6
        first_printer_hl_pattern = Pattern('first_printer_highlight.png')
        second_printer_hl_pattern = Pattern('second_printer_highlight.png')
        second_printer_white_pattern = Pattern('second_printer_white.png')

        """ STEP 1 """

        test_page_local = self.get_asset_path('pdf.pdf')
        navigate(test_page_local)

        navigated_to_pdf_url = exists(pdf_logo_pattern, 5)

        assert_true(self, navigated_to_pdf_url, 'PDF URL loaded successfully.')

        """ END STEP 1 """

        """ STEP 2 """

        open_find()

        # Remove all text from the Find Toolbar

        edit_select_all()
        edit_delete()

        find_toolbar_is_opened = exists(find_toolbar_pattern, 5)

        assert_true(self, find_toolbar_is_opened, 'The Find Toolbar is successfully displayed '
                                                  'by pressing CTRL + F / Cmd + F,.')

        """ END STEP 2 """

        """ STEP 3 """

        type('printer')
        type(Key.ENTER)

        word_printer_hl_exists = exists(first_printer_hl_pattern, 5)
        word_printer_white_exists = exists(second_printer_white_pattern, 5)

        assert_true(self, (word_printer_hl_exists and word_printer_white_exists),
                    'All the matching words / characters are found.')

        """ END STEP 3 """

        """ STEP 4 """

        first_occurrence_highlighted = exists(first_printer_hl_pattern, 5)

        assert_true(self, first_occurrence_highlighted, 'First occurrence highlighted')

        # Switch to next occurrence
        find_next()

        second_occurrence_highlighted = exists(second_printer_hl_pattern, 5)

        assert_true(self, second_occurrence_highlighted, 'Second occurrence highlighted')

        # Get back to first occurrence
        find_previous()

        """ END STEP 4 """

        """ STEP 5 """

        before_scroll_first_exists = exists(first_printer_hl_pattern, 5)

        for i in range(4):
            scroll_down()

        for i in range(4):
            scroll_up()

        after_scroll_first_exists = exists(first_printer_hl_pattern, 5)

        assert_true(self, before_scroll_first_exists and after_scroll_first_exists,
                    'Occurrence exists after scroll up and down. No checkboarding is present')

        """ END STEP 5 """
