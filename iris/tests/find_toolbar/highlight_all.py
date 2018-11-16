# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = '"Highlight All" button works properly'
        self.test_case_id = '0'
        self.test_suite_id = '0'
        self.locales = ['en-US']

    def run(self):
        """
        "Highlight All" button works properly

        STEP 1:
            DESCRIPTION:
                Open Firefox and navigate to a wikipedia website

            EXPECTED:
                The page is successfully loaded.

        STEP 2:
            DESCRIPTION:
                Open the Find toolbar.

            EXPECTED:
                Find Toolbar is opened.

        STEP 3:
            DESCRIPTION:
                Enter a search term and press ENTER.

            EXPECTED:
                All the matching words/characters are found. The first one has a green background highlighted, and the others are not highlighted.

        STEP 4:
            DESCRIPTION:
                Click on "Highlight All".

            EXPECTED:
                All the matching words/characters are found. The first one has a green background highlighted, and the other ones a pink background.

        STEP 5:
            DESCRIPTION:
                Press on ENTER or navigate through the results using F3 / SHIFT+F3.

            EXPECTED:
                The next matching words/characters have a green background highlighted and the other ones a pink background.


        NOTES:
            Initial version - Dmitry Bakaev  - 13-Nov-2018
            Code review complete - Paul Prokhorov - 13-Nov-2018
        """

        soap_label_pattern = Pattern('soap_label.png')
        see_label_pattern = Pattern('see_label.png')
        see_label_pink_pattern = Pattern('see_label_pink.png')
        see_label_unhighlited_pattern = Pattern('see_label_unhighlited.png')
        see_label_capital_selected_pattern = Pattern('see_label_capital_selected.png')
        see_also_label_pattern = Pattern('see_also_label.png')
        find_in_page_icon_pattern = Pattern('find_in_page_icon.png')
        highligh_all_button_pattern = Pattern('highlight_all_button.png')

        """ STEP 1 """

        navigate('https://en.wikipedia.org/wiki/SOAP')
        soap_label_exists = exists(soap_label_pattern, 20)

        assert_true(self, soap_label_exists, 'The page is successfully loaded.')

        """ END STEP 1 """

        """ STEP 2 """

        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(find_in_page_icon_pattern, 10)

        assert_true(self, find_toolbar_opened, 'Find Toolbar is opened.')

        """ END STEP 2 """

        """ STEP 3 """

        type('see', interval=1)
        type(Key.ENTER)

        selected_label_exists = exists(see_label_pattern, 5)
        unhighlighted_label_exists = exists(see_label_unhighlited_pattern, 5)

        assert_true(self, selected_label_exists, 'The first one has a green background highlighted.')
        assert_true(self, unhighlighted_label_exists,
                    'The others are not highlighted.')

        """ END STEP 3 """

        """ STEP 4 """

        click(highligh_all_button_pattern)

        first_label_is_green = exists(see_label_pattern, 5)
        other_label_pink = exists(see_label_pink_pattern, 5)

        assert_true(self, first_label_is_green, 'The first one has a green background highlighted')
        assert_true(self, other_label_pink, 'The other one has a pink background highlighted')

        """ END STEP 4 """

        """ STEP 5 """

        find_next()
        find_next()

        next_matching_green_exists = exists(see_label_capital_selected_pattern, 5)
        next_matching_pink_exists = exists(see_also_label_pattern, 5)

        assert_true(self, next_matching_green_exists,
                    'The next matching words/characters have a green background highlighted')
        assert_true(self, next_matching_pink_exists,
                    'The next matching words/characters have a pink background highlighted')

        """ END STEP 5 """
