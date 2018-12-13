# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *
from iris.api.core import mouse


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Delete history from Library context menu'
        self.test_case_id = '178346'
        self.test_suite_id = '2000'

    def setup(self):
        """Test case setup

        This overrides the setup method in the BaseTest class, so that it can use a brand new profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.BRAND_NEW

        return

    def run(self):
        history_mozilla_pattern = Pattern('library_bookmarks_mozilla.png')
        history_pattern = Library.HISTORY
        history_today_pattern = Library.HISTORY_TODAY

        # Open a page to create some history.
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, expected_1, 'Mozilla page loaded successfully.')

        # Open History.
        open_library()
        expected_2 = exists(history_pattern, 10)
        assert_true(self, expected_2, 'History section is displayed.')

        # Expand History.
        double_click(history_pattern)
        expected_3 = exists(history_today_pattern, 10)
        assert_true(self, expected_3, 'Today history option is available.')

        # Verify if Mozilla page is present in Today History.
        mouse.mouse_move(Location(SCREEN_WIDTH / 4 + 100, SCREEN_HEIGHT / 4))
        click(history_today_pattern)
        expected_4 = exists(history_mozilla_pattern, 10)
        assert_true(self, expected_4, 'Mozilla page is displayed in the History list successfully.')

        # Delete Mozilla page from Today's History.
        right_click(history_mozilla_pattern)
        type(text='d')

        try:
            expected_5 = wait_vanish(history_mozilla_pattern.similar(0.9), 10)
            assert_true(self, expected_5, 'Mozilla page was deleted successfully from the history.')
        except FindError:
            raise FindError('Mozilla page is still displayed in the history.')

        click_window_control('close')
