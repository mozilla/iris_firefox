# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.api.core import mouse
from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Custom sections selected in \'Clear Recent History\' window'
        self.test_case_id = '172047'
        self.test_suite_id = '2000'
        self.locales = ['en-US']

    def setup(self):
        """Test case setup

        This overrides the setup method in the BaseTest class, so that it can use a brand new profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.BRAND_NEW
        self.set_profile_pref({'datareporting.policy.firstRunURL': ''})

        return

    def run(self):
        clear_recent_history_window_pattern = History.CLearRecentHistory.CLEAR_RECENT_HISTORY_TITLE
        clear_now_button_pattern = History.CLearRecentHistory.CLEAR_NOW
        search_unchecked_box_pattern = Utils.UNCHECKEDBOX
        history_pattern = Sidebar.HistorySidebar.SIDEBAR_HISTORY_TITLE
        searched_history_logo_pattern = Sidebar.HistorySidebar.EXPLORED_HISTORY_ICON
        privacy_logo_pattern = Pattern('privacy_logo.png')
        manage_data_pattern = Pattern('manage_data_button.png')
        manage_data_title_pattern = Pattern('manage_cookies_and_site_data_table_heads.png').similar(0.7)
        saved_logins_button_pattern = Pattern('saved_logins_button.png')
        saved_logins_window_pattern = Pattern('saved_logins_table_heads.png').similar(0.7)
        ago_word_pattern = Pattern('ago_pattern.png').similar(0.95)
        empty_saved_logins_pattern = Pattern('empty_saved_logins.png')

        # Open the 'Clear Recent History' window and uncheck all the items.
        for step in open_clear_recent_history_window():
            assert_true(self, step.resolution, step.message)

        if Settings.get_os() == Platform.MAC:
            expected = exists(search_unchecked_box_pattern, 10)
        else:
            expected = exists(search_unchecked_box_pattern.similar(0.9), 10)

        while expected:
            assert_true(self, expected, 'Unchecked box exists.')
            click(search_unchecked_box_pattern)
            expected = exists(search_unchecked_box_pattern, 10)

        # Clear the Clear recent history.
        expected = exists(clear_now_button_pattern, 10)
        assert_true(self, expected, '\"Clear Now\" button found.')
        click(clear_now_button_pattern)

        # Check that the Clear Recent History window was dismissed properly.
        try:
            expected = wait_vanish(clear_recent_history_window_pattern.similar(0.9), 10)
            assert_true(self, expected, 'Clear Recent History window was dismissed properly.')
        except FindError:
            raise FindError('Clear Recent History window is still open.')

        # ASSERTS.

        # Open the History sidebar.
        history_sidebar()
        expected = exists(history_pattern, 10)
        assert_true(self, expected, 'History sidebar is opened.')

        # Check that the history is empty.
        region = Region(0, SCREEN_HEIGHT / 7, SCREEN_WIDTH / 7, SCREEN_HEIGHT / 5)
        expected = region.exists(searched_history_logo_pattern, 10)
        assert_false(self, expected, 'History is empty.')

        # Close the History sidebar.
        history_sidebar()
        expected = exists(history_pattern, 10)
        assert_false(self, expected, 'History sidebar is closed.')

        # Check that cookies were deleted.
        # Access the privacy page.
        navigate('about:preferences#privacy')
        expected = exists(privacy_logo_pattern, 10)
        assert_true(self, expected, 'Privacy page has been accessed.')

        # Scroll in page and access the "Saved Logins" button.
        mouse.mouse_move(Location(SCREEN_WIDTH / 4 + 100, SCREEN_HEIGHT / 4))
        time.sleep(Settings.SYSTEM_DELAY)
        expected = exists(saved_logins_button_pattern, 10)
        while not expected:
            mouse.scroll(-10)
            expected = exists(saved_logins_button_pattern, 2)
        assert_true(self, expected, '\"Saved Logins\" button has been found.')
        click(saved_logins_button_pattern)

        # Check that "Saved Logins" window is displayed.
        region = Region(SCREEN_WIDTH / 7, SCREEN_HEIGHT / 4, SCREEN_WIDTH, SCREEN_HEIGHT / 4)
        expected = region.exists(saved_logins_window_pattern, 10)
        assert_true(self, expected, '\"Saved Logins\" window is displayed.')

        # Check that the "Saved Logins" window is empty.
        expected = exists(empty_saved_logins_pattern.similar(0.7), 10)
        assert_true(self, expected, 'There are no logins saved.')

        # Close and check the "Saved Logins" window.
        type(Key.ESC)
        expected = exists(saved_logins_window_pattern, 10)
        assert_false(self, expected, '\"Saved Logins\" window is NOT displayed.')

        # Access the "Manage Data" window.
        expected = exists(manage_data_pattern, 10)
        assert_true(self, expected, '\"Manage Data\" button has been found.')
        click(manage_data_pattern)

        # Check that "Manage Cookies and Site Data" window is displayed.
        expected = region.exists(manage_data_title_pattern, 10)
        assert_true(self, expected, '\"Manage Cookies and Site Data\" window is displayed.')

        # Check that the "Manage Cookies and Site Data" window is empty.
        expected = exists(ago_word_pattern, 10)
        assert_false(self, expected, 'Cookies were deleted.')

        # Close and check the "Manage Cookies and Site Data" window.
        type(Key.ESC)
        expected = exists(manage_data_title_pattern, 10)
        assert_false(self, expected, '\"Manage Cookies and Site Data\" window is NOT displayed.')
