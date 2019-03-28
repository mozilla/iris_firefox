# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Copy a website from the Library - History menu and Paste it in to the URL bar.'
        self.test_case_id = '174047'
        self.test_suite_id = '2000'

    def setup(self):
        """Test case setup

        Override the setup method to use a pre-canned bookmarks profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        mozilla_bookmark_focus = Pattern('mozilla_bookmark_focus.png')

        # Open some page to create some history for today.
        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        close_tab()

        # Open History and check if is populated with Mozilla page.
        open_history_library_window()

        expected_1 = exists(mozilla_bookmark_focus, 10)
        assert_true(self, expected_1, 'Mozilla page is displayed in the History list successfully.')

        # Copy a website from the History section and paste it into the URL bar.
        right_click(mozilla_bookmark_focus)
        type(text='c')
        click_window_control('close')
        select_location_bar()
        edit_paste()
        type(Key.ENTER)

        # Check that the page was opened successfully.
        expected_2 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, expected_2, 'Mozilla page loaded successfully.')
