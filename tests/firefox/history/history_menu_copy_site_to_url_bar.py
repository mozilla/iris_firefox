# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Copy a website from the Library - History menu and Paste it in to the URL bar.',
        locale=['en-US'],
        test_case_id='174047',
        test_suite_id='2000',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        mozilla_bookmark_focus = Pattern('mozilla_bookmark_focus.png')

        # Open some page to create some history for today.
        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        close_tab()

        # Open History and check if is populated with Mozilla page.
        open_history_library_window()

        expected_1 = exists(mozilla_bookmark_focus, 10)
        assert expected_1, 'Mozilla page is displayed in the History list successfully.'

        # Copy a website from the History section and paste it into the URL bar.
        right_click_and_type(mozilla_bookmark_focus, keyboard_action='c')

        click_window_control('close')

        time.sleep(Settings.DEFAULT_UI_DELAY)

        select_location_bar()
        edit_paste()
        time.sleep(Settings.DEFAULT_UI_DELAY)
        type(Key.ENTER)

        # Check that the page was opened successfully.
        expected_2 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected_2, 'Mozilla page loaded successfully.'
