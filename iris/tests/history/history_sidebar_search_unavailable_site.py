# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'Search in History sidebar for an unavailable website.'
        self.test_case_id = '119441'
        self.test_suite_id = '2000'

    def setup(self):
        """Test case setup

        This overrides the setup method in the BaseTest class, so that it can use a brand new profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.BRAND_NEW
        return

    def run(self):
        search_history_box = 'search_history_box.png'
        expand_button_history_sidebar = 'expand_button_history_sidebar.png'
        history_empty = 'history_empty.png'

        # Open a page to create some history.
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, expected_1, 'Mozilla page loaded successfully.')

        # Open the History sidebar.
        history_sidebar()
        expected_2 = exists(search_history_box, 10)
        assert_true(self, expected_2, 'Sidebar was opened successfully.')
        expected_3 = exists(expand_button_history_sidebar, 10)
        assert_true(self, expected_3, 'Expand history button displayed properly.')
        click(expand_button_history_sidebar)
        click(search_history_box)

        # Check that an unavailable page is not found in the History list.
        paste('test')
        type(Key.TAB)
        expected_4 = exists(history_empty, 10)
        assert_true(self, expected_4, 'The page wasn\'t found in the History list.')
