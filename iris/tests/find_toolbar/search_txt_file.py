# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Search on a text file (.txt)'
        self.test_case_id = '127273'
        self.test_suite_id = '2085'
        self.locales = ['en-US']

    def run(self):

        """
        Search on a text file (.txt)

        STEP 1:
            DESCRIPTION:
                Open Firefox and open a [.txt page](https://wordpress.org/plugins/about/readme.txt)
                * provided url doesn't contain *.txt file. Opened
                https://www.kernel.org/doc/Documentation/dmaengine/dmatest.txt instead

            EXPECTED:
                The page is loaded.

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
                Navigate throught found items (F3, SHIFT+F3)

            EXPECTED:
                The green box is moved with the current item.

        STEP 5:
            DESCRIPTION:
                Scroll the page up and down.

            EXPECTED:
                No checkboarding is present. The performance is good.


        NOTES:
            Initial version - Pavel Ciapa  - 13-Nov-2018
            Code review complete - Dmitry Bakaev - 16-Nov-2018

        """

        find_toolbar_pattern = Pattern('find_toolbar_text.png')
        txt_page_title_pattern = Pattern('txt_page_title.png')
        txt_page_title_pattern.similarity = 0.6

        text_first_occurrence_hl_pattern = Pattern('txt_text_first_occurrence_hl.png')
        text_first_occurrence_white_pattern = Pattern('txt_text_first_occurrence_white.png')
        text_second_occurrence_hl_pattern = Pattern('txt_text_second_occurrence_hl.png')
        text_second_occurrence_white_pattern = Pattern('txt_text_second_occurrence_white.png')

        """ STEP 1 """

        test_page_local = self.get_asset_path('dmatest.txt')
        navigate(test_page_local)

        txt_page_title_pattern_exists = exists(txt_page_title_pattern, 5)

        assert_true(self, txt_page_title_pattern_exists, 'The page is successfully loaded.')

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

        type('Part')

        text_first_occurrence_hl_exists = exists(text_first_occurrence_hl_pattern, 5)
        text_second_occurrence_white_exists = exists(text_second_occurrence_white_pattern, 5)

        assert_true(self, (text_first_occurrence_hl_exists and text_second_occurrence_white_exists),
                    'All the matching words/characters are found.')

        """ END STEP 3 """

        """ STEP 4 """

        text_first_occurrence_hl_exists = exists(text_first_occurrence_hl_pattern, 5)
        text_second_occurrence_white_exists = exists(text_second_occurrence_white_pattern, 5)

        assert_true(self, text_first_occurrence_hl_exists and text_second_occurrence_white_exists,
                    'First occurence highlightened')

        # Go to next occurrence
        find_next()

        text_first_occurrence_white_exists = exists(text_first_occurrence_white_pattern, 5)
        text_second_occurrence_hl_exists = exists(text_second_occurrence_hl_pattern, 5)

        assert_true(self, text_first_occurrence_white_exists and text_second_occurrence_hl_exists,
                    'Second occurrence highlightened')

        # Get back to first occurrence
        find_previous()

        """ END STEP 4 """

        """ STEP 5 """

        text_first_occurrence_exists_before_scroll = exists(text_first_occurrence_hl_pattern, 5)

        # Move found word away of screen and back
        for i in range(4):
            scroll_down()

        for i in range(4):
            scroll_up()

        text_first_occurrence_exists_after_scroll = exists(text_first_occurrence_hl_pattern, 5)

        assert_true(self, text_first_occurrence_exists_before_scroll and text_first_occurrence_exists_after_scroll,
                    'Occurrence exists after scroll up and down')

        """ END STEP 5 """