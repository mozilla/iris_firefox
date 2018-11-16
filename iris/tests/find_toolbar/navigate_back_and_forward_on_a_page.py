# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Navigate back and forward on a page'
        self.test_case_id = '0'
        self.test_suite_id = '0'
        self.locales = ['en-US']

    def run(self):
        """
        Navigate back and forward on a page

        STEP 1:
            DESCRIPTION:
                Open Firefox and navigate to some popular websites on the same tab (Ebay, Reddit, etc).

            EXPECTED:
                The page is successfully loaded.

        STEP 2:
            DESCRIPTION:
                Open the Find Toolbar.

            EXPECTED:
                Find Toolbar is opened.

        STEP 3:
            DESCRIPTION:
                Navigate back to the previous page (Click the left arrow next to the URL bar).

            EXPECTED:
                Find Toolbar persist on this page.

        STEP 4:
            DESCRIPTION:
                Navigate forward to the next page (Click the right arrow next to the URL bar).

            EXPECTED:
                Find Toolbar persist on this page.

        NOTES:
            Initial version - Pavel Ciapa  - 11-Nov-2018
            Code review complete - Paul Prokhorov - 15-Nov-2018
        """

        find_toolbar_pattern = Pattern('find_toolbar_text.png')
        wiki_logo = Pattern('wiki_logo_icon.png')
        arrow_back_button_pattern = Pattern('arrow_back_button.png')
        arrow_forward_button_pattern = Pattern('arrow_forward_button.png')
        new_tab_icon_pattern = Pattern('new_tab_icon.png')

        """ STEP 1 """

        new_tab()
        navigate('https://www.wikipedia.org/')
        page_loaded = wait(wiki_logo, 20)

        assert_true(self, page_loaded, 'The website successfully loaded.')

        """ END STEP 1 """

        """ STEP 2 """

        open_find()

        # Remove all text from the Find Toolbar
        edit_select_all()
        edit_delete()

        find_toolbar_is_opened = wait(find_toolbar_pattern, 15)
        assert_true(self, find_toolbar_is_opened, 'The find toolbar is opened')

        """ END STEP 2 """

        """ STEP 3 """

        # Navigate back to the previous page
        wait(arrow_back_button_pattern, 10)

        click(arrow_back_button_pattern, 2)
        find_toolbar_is_opened_previous_page = wait(new_tab_icon_pattern, 10)

        assert_true(self, find_toolbar_is_opened_previous_page, 'The find toolbar is present on the previous page')

        """ END STEP 3 """

        """ STEP 4 """

        # Navigate forward to the page
        click(arrow_forward_button_pattern)
        find_toolbar_is_opened_next_page = wait(wiki_logo, 10)

        assert_true(self, find_toolbar_is_opened_next_page, 'The find toolbar is present on the next page')

        """ END STEP 4 """
