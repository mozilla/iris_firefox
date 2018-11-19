# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Search for a long String'
        self.test_case_id = '127244'
        self.test_suite_id = '2085'
        self.locales = ['en-US']

    def run(self):
        """
        Search for a long String

        STEP 1:
            DESCRIPTION:
                Open Firefox and navigate to a popular website (Google.com, Amazon.com, NYTimes etc).

            EXPECTED:
                The page is successfully loaded.

        STEP 2:
            DESCRIPTION:
                Open the Find toolbar.

            EXPECTED:
                Find Toolbar is opened.

        STEP 3:
            DESCRIPTION:
                Search for a long term that appears on the page.

            EXPECTED:
                All the matching words/characters are found. The first one has a green background highlighted, and the others are not highlighted.

        NOTES:
            Initial version - Dmitry Bakaev  - 14-Nov-2018
            Code review complete - Paul Prokhorov - 15-Nov-2018
        """

        find_in_page_icon_pattern = Pattern('find_in_page_icon.png')
        long_word_selected_label_pattern = Pattern('long_word_selected_label.png')
        long_word_unselected_label_pattern = Pattern('long_word_unselected_label.png')

        """ STEP 1 """

        test_page_local = self.get_asset_path('long_word.html')
        navigate(test_page_local)

        start_label_exists = exists(long_word_unselected_label_pattern, 30)

        assert_true(self, start_label_exists, 'The page is successfully loaded.')

        """ END STEP 1 """

        """ STEP 2 """

        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(find_in_page_icon_pattern, 10)

        assert_true(self, find_toolbar_opened, 'Find Toolbar is opened.')

        """ END STEP 2 """

        """ STEP 3 """

        type('Pneumonoultramicroscopicsilicovolcanoconiosis')

        selected_label_exists = exists(long_word_selected_label_pattern, 5)
        unselected_label_exists = exists(long_word_unselected_label_pattern, 5)

        assert_true(self, selected_label_exists, 'The first one has a green background highlighted.')
        assert_true(self, unselected_label_exists, 'The others are not highlighted.')

        """ END STEP 3 """
