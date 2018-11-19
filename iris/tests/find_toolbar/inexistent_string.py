# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Search for an inexistent String on the page'
        self.test_case_id = '127245'
        self.test_suite_id = '2085'
        self.locales = ['en-US']

    def run(self):
        """
        Search for an inexistent String on the page

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
                Search for an inexistent String on the page.

            EXPECTED:
                In the Toolbar the input field has a red background and the "Phrase not found" message appears on the Find Toolbar.

        STEP 4:
            DESCRIPTION:
                Tap the "Find next", "Find previous" arrows from the toolbar.

            EXPECTED:
                The arrows are disabled.

        NOTES:
            Initial version - Dmitry Bakaev  - 14-Nov-2018
            Code review complete - Paul Prokhorov - 15-Nov-2018
        """

        find_in_page_icon_pattern = Pattern('find_in_page_icon.png')
        soap_label_pattern = Pattern('soap_label.png')
        phrase_not_found_label_pattern = Pattern('phrase_not_found_label.png')
        arrow_down_button_pattern = Pattern('arrow_down_button.png')
        arrow_up_button_pattern = Pattern('arrow_up_button.png')
        merge_red_textbox_pattern = Pattern('merge_red_textbox.png')

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

        type('merge', interval=1)

        red_textbox_exists = exists(merge_red_textbox_pattern, 5)
        label_not_found = exists(phrase_not_found_label_pattern, 5)

        assert_true(self, red_textbox_exists, 'input field has a red background')
        assert_true(self, label_not_found, 'Phrase not found appears')

        """ END STEP 3 """

        """ STEP 4 """

        click(arrow_down_button_pattern)
        click(arrow_up_button_pattern)

        red_textbox_exists = exists(merge_red_textbox_pattern, 5)

        assert_true(self, red_textbox_exists, 'The arrows do not change the state.')

        """ END STEP 4 """
