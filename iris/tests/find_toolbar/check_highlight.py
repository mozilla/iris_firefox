# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Check the highlight of the found item'
        self.test_case_id = '127240'
        self.test_suite_id = '2085'
        self.locales = ['en-US']

    def run(self):
        """
        Check the highlight of the found item

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
                Check the position of the highlighted term.

            EXPECTED:
                The highlight of the found term should not affect the visibility of other words or letters.


        NOTES:
            Initial version - Dmitry Bakaev  - 13-Nov-2018
            Code review complete - Paul Prokhorov  - 13-Nov-2018
        """

        soap_label_pattern = Pattern('soap_label.png')
        see_label_pattern = Pattern('see_label.png')
        see_label_unhighlited_pattern = Pattern('see_label_unhighlited.png')
        find_in_page_icon_pattern = Pattern('find_in_page_icon.png')

        """ STEP 1 """

        test_page_local = self.get_asset_path('wiki_soap.html')
        navigate(test_page_local)

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

        """ STEP 3 / 4 """

        type('see', interval=1)
        type(Key.ENTER)

        selected_label_exists = exists(see_label_pattern, 5)
        unhighlighted_label_exists = exists(see_label_unhighlited_pattern, 5)

        assert_true(self, selected_label_exists, 'The first one has a green background highlighted.')
        assert_true(self, unhighlighted_label_exists,
                    'The others are not highlighted.')

        """ END STEP 3 / 4 """
