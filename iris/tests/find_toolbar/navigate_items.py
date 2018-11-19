# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Navigate through found items'
        self.test_case_id = '127249'
        self.test_suite_id = '2085'
        self.locales = ['en-US']

    def run(self):
        """
        Navigate through found items

        STEP 1:
            DESCRIPTION:
                Open Firefox and navigate to a popular website (Ebay, Reddit, etc).

            EXPECTED:
                The page is successfully loaded.

        STEP 2:
            DESCRIPTION:
                Open the Find toolbar.

            EXPECTED:
                Find Toolbar is opened.

        STEP 3:
            DESCRIPTION:
                Search for a term that appears more than once in the page.

            EXPECTED:
                All the matching words/characters are found. The first one has a green background highlighted, and the others are not highlighted.

        STEP 4:
            DESCRIPTION:
                Navigate forward and back throught found items using the toolbar arrows.

            EXPECTED:
                Navigation works fine. The current item is highlighted with green. No functional or visible issue appears.

        STEP 5:
            DESCRIPTION:
                Inspect if the number of the current highlighted item from the Find Toolbar changes when navigating. (e.g 1 of 12 matches > 2 of 12 matches)

            EXPECTED:
                The number of the highlighted item changes when navigating.


        NOTES:
            Initial version - Dmitry Bakaev  - 19-Nov-2018
            Code review complete - -
        """

        soap_label_pattern = Pattern('soap_label.png')
        see_label_pattern = Pattern('see_label.png')
        see_label_unhighlited_pattern = Pattern('see_label_unhighlited.png')
        find_in_page_icon_pattern = Pattern('find_in_page_icon.png')

        arrow_up_button_pattern = Pattern('arrow_up_button.png')
        arrow_down_button_pattern = Pattern('arrow_down_button.png')
        cleaning_see_label_pattern = Pattern('cleaning_see_label.png')
        one_of_five_label_pattern = Pattern('1_of_5_matches_label.png')
        two_of_five_lable_pattern = Pattern('2_of_5_matches_label.png')

        """ STEP 1 """

        wikipedia_page_local = self.get_asset_path('soap.html')
        navigate(wikipedia_page_local)
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

        click(arrow_up_button_pattern)
        cleaning_see_label_exists = exists(cleaning_see_label_pattern, 5)

        assert_true(self, cleaning_see_label_exists, 'Navigation up works fine.')

        click(arrow_down_button_pattern)
        selected_label_exists = exists(see_label_pattern, 5)

        assert_true(self, selected_label_exists, 'Navigation down works fine.')



        """ END STEP 4 """

        """ STEP 5 """

        click(arrow_up_button_pattern)
        one_of_five_label_exists = exists(one_of_five_label_pattern, 5)

        assert_true(self, one_of_five_label_exists, 'The number of the highlighted item changes when navigating')

        click(arrow_down_button_pattern)
        two_of_five_label_exists = exists(two_of_five_lable_pattern, 5)

        assert_true(self, two_of_five_label_exists, 'The number of the highlighted item changes when navigating.')



        """ END STEP 5 """

