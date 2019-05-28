# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Use \'Open in a New Window\' button from the contextual options.',
        locale=['en-US'],
        test_case_id='174040',
        test_suite_id='2000'
    )
    def run(self, firefox):
        iris_bookmark_pattern = Pattern('iris_bookmark.png')
        show_all_history_pattern = History.HistoryMenu.SHOW_ALL_HISTORY
        new_tab_pattern = Pattern('new_tab.png')
        mozilla_bookmark_focus_pattern = Pattern('mozilla_bookmark_focus.png')

        # Open a page to create some history.
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        expected = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected is True, 'Mozilla page loaded successfully.'

        new_tab()
        previous_tab()
        close_tab()

        # Open History and check if it is populated with the Iris page.
        open_library_menu('History')

        right_upper_corner = Screen().new_region(Screen.SCREEN_WIDTH / 2, 0, Screen.SCREEN_WIDTH / 2,
                                                 Screen.SCREEN_HEIGHT / 2)

        expected = right_upper_corner.exists(iris_bookmark_pattern, 10)
        assert expected is True, 'Iris page is displayed in the History menu list.'

        click(show_all_history_pattern, 1)

        expected = exists(mozilla_bookmark_focus_pattern, 10)
        assert expected is True, 'Mozilla page is displayed in the Recent History list.'

        # Open page in new window.
        right_click(mozilla_bookmark_focus_pattern)
        type(text='n')

        # Make sure that the selected website is opened in a new window.
        expected = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected is True, 'Mozilla page loaded successfully.'

        expected = exists(new_tab_pattern, 5)
        assert expected is False, 'about:newtab page is not visible in the new opened window.'

        close_window()
        click_window_control('close')
