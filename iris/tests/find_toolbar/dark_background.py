# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Check the highlight of the found items on a page with dark background'
        self.test_case_id = '127242'
        self.test_suite_id = '2085'
        self.locales = ['en-US']

    def run(self):
        """
        Check the highlight of the found items on a page with dark background

        STEP 1:
            DESCRIPTION:
                Open Firefox and navigate to a page with dark background, for example [this page](http://www.vanschneider.com)

            EXPECTED:
                The page is successfully loaded.

        STEP 2:
            DESCRIPTION:
                Open the Find toolbar.

            EXPECTED:
                Find Toolbar is opened.

        STEP 3:
            DESCRIPTION:
                Search for a term that appears in the page.

            EXPECTED:
                All the matching words/characters are found. The first one has a green background highlighted, and the others are not highlighted.

        STEP 4:
            DESCRIPTION:
                Check the visibility of the highlighted term.

            EXPECTED:
                The highlight of the matches should be visible.

        NOTES:
            Initial version - Dmitry Bakaev  - 14-Nov-2018
            Code review complete - Paul Prokhorov - 14-Nov-2018
        """

        find_in_page_icon_pattern = Pattern('find_in_page_icon.png')
        work_in_label_pattern = Pattern('work_in_selected_label.png')
        instagram_unselected_pattern = Pattern('instagram_unselected_label.png')

        """ STEP 1 """

        test_page_local = self.get_asset_path('dark_backgound.html')
        navigate(test_page_local)

        page_loaded = exists(instagram_unselected_pattern, 100)

        assert_true(self, page_loaded, 'The page is successfully loaded.')

        """ END STEP 1 """

        """ STEP 2 """

        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(find_in_page_icon_pattern, 10)

        assert_true(self, find_toolbar_opened, 'Find Toolbar is opened.')

        """ END STEP 2 """

        """ STEP 3 / 4 """

        type('in', interval=1)

        selected_label_exists = exists(work_in_label_pattern, 15)
        unselected_label_exists = exists(instagram_unselected_pattern, 5)

        assert_true(self, selected_label_exists, 'The first one has a green background highlighted.')
        assert_true(self, unselected_label_exists, 'The others are not highlighted.')

        """ END STEP 3 / 4 """
