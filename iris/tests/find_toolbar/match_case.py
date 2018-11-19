# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = '"Match Case" button works properly'
        self.test_case_id = '127452'
        self.test_suite_id = '2085'
        self.locales = ['en-US']

    def run(self):
        """
        "Match Case" button works properly

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
                Enter a search term and activate "Match Case" and press ENTER.

            EXPECTED:
                All the matching words/characters are found. The first one has a green background highlighted, and the others are not highlighted.

        STEP 4:
            DESCRIPTION:
                Press on ENTER or navigate through the results using F3 / SHIFT+F3.

            EXPECTED:
                The next matching words/characters have a green background highlighted and the others are not highlighted.

        NOTES:
            Initial version - Dmitry Bakaev  - 13-Nov-2018
            Code review complete - Paul Prokhorov - 13-Nov-2018
        """

        find_in_page_icon_pattern = Pattern('find_in_page_icon.png')
        soap_label_pattern = Pattern('soap_label.png')
        match_case_button_pattern = Pattern('match_case_button.png')
        soap_xml_label_pattern = Pattern('soap_xml_label.png')
        soap_envelope_label_selected_pattern = Pattern('soap_envelope_label_selected.png')
        soap_label_selected_pattern = Pattern('soap_label_selected.png')

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

        """ STEP 3 """

        type('soap', interval=1)
        click(match_case_button_pattern)
        find_next()

        selected_label_exists = exists(soap_envelope_label_selected_pattern, 5)
        unselected_label_exists = exists(soap_xml_label_pattern, 5)

        assert_true(self, selected_label_exists, 'The first one has a green background highlighted.')
        assert_true(self, unselected_label_exists,
                    'The others are not highlighted.')

        """ END STEP 3 """

        """ STEP 4 """

        find_next()

        first_label_is_green = exists(soap_label_selected_pattern, 5)
        other_label_is_unhighlighted = exists(soap_xml_label_pattern, 5)

        assert_true(self, first_label_is_green, 'The next matching words/characters have a green background highlighted')
        assert_true(self, other_label_is_unhighlighted, 'The other is not highlighted')

        """ END STEP 4 """
