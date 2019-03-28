# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Verify if the deleted page from History is retained in auto-complete.'
        self.test_case_id = '174049'
        self.test_suite_id = '2000'
        self.locales = ['en-US']

    def run(self):
        local_server_autocomplete = Pattern('local_server_autocomplete.png')
        mozilla_bookmark_focus = Pattern('mozilla_bookmark_focus.png')
        pocket_autocomplete = Pattern('pocket_autocomplete.png')
        mozilla_autocomplete = Pattern('mozilla_autocomplete.png')

        # Visit two pages from the same domain at least two times to make sure that auto-fill is working in the URL bar.
        new_tab()
        navigate(LocalWeb.POCKET_TEST_SITE)
        navigate(LocalWeb.POCKET_TEST_SITE)
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        select_location_bar()
        paste('127.0.0.1:2000/p')

        expected_1 = exists(pocket_autocomplete, 10)
        assert_true(self, expected_1, 'Pocket page is auto-completed successfully.')

        click(NavBar.FORWARD_BUTTON.target_offset(-50, 0))

        select_location_bar()
        paste('127.0.0.1:2000/m')
        expected_2 = exists(mozilla_autocomplete, 10)
        assert_true(self, expected_2, 'Mozilla page is auto-completed successfully.')

        close_tab()
        new_tab()

        # Open History and check if is populated with Mozilla page.
        open_history_library_window()

        expected_3 = exists(mozilla_bookmark_focus, 10)
        assert_true(self, expected_3, 'Mozilla page is displayed in the History list successfully.')

        # Delete Mozilla page.
        right_click(mozilla_bookmark_focus)
        type(text='d')

        try:
            expected_4 = wait_vanish(mozilla_bookmark_focus, 10)
            assert_true(self, expected_4, 'Mozilla page was deleted successfully from the history.')
        except FindError:
            raise FindError('Mozilla page is still displayed in the history.')

        click_window_control('close')

        # Check that the local server is still auto-completed in the URL bar.
        select_location_bar()
        paste('127')

        expected_5 = exists(local_server_autocomplete, 10)
        assert_true(self, expected_5, 'Local server is auto-completed successfully.')
