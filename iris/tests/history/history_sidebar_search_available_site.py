# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'Search in History sidebar for an available website.'

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
        history_sidebar_focus = 'history_sidebar_focus.png'

        # Open a page to create some history.
        navigate(LocalWeb.FOCUS_TEST_SITE)
        expected_1 = exists(LocalWeb.FOCUS_LOGO, 10)
        assert_true(self, expected_1, 'Focus page loaded successfully.')

        # Open the History sidebar.
        history_sidebar()
        expected_2 = exists(search_history_box, 10)
        assert_true(self, expected_2, 'Sidebar was opened successfully.')
        expected_3 = exists(expand_button_history_sidebar, 10)
        assert_true(self, expected_3, 'Expand history button displayed properly.')
        click(expand_button_history_sidebar)
        click(search_history_box)

        # Check that Focus page is found in the History list.
        paste('focus')
        type(Key.TAB)
        expected_4 = exists(history_sidebar_focus, 10)
        assert_true(self, expected_4, 'Focus page was found in the History list successfully.')
