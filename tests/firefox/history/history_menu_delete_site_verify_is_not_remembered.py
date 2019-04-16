# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Verify if the deleted page from History is not retained in auto-complete.',
        locale='[en-US]',
        test_case_id='216273',
        test_suite_id='2000'
    )
    def test_run(self, firefox):
        mozilla_bookmark_focus = Pattern('mozilla_bookmark_focus.png')
        mozilla_autocomplete = Pattern('mozilla_autocomplete.png')

        # Visit a page at least two times to make sure that auto-fill is working in the URL bar.
        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        select_location_bar()
        paste('http://127.0.0.1:2000/m')

        expected_1 = exists(mozilla_autocomplete, 10)
        assert expected_1, 'Mozilla page is auto-completed successfully.'

        close_tab()
        new_tab()

        # Open History and check if is populated with Mozilla page.
        open_history_library_window()

        expected_2 = exists(mozilla_bookmark_focus, 10)
        assert expected_2, 'Mozilla page is displayed in the History list successfully.'

        # Delete Mozilla page.
        right_click_and_type(mozilla_bookmark_focus, keyboard_action='d')


        try:
            expected_3 = wait_vanish(mozilla_bookmark_focus, 10)
            assert expected_3, 'Mozilla page was deleted successfully from the history.'
        except FindError:
            raise FindError('Mozilla page is still displayed in the history.')

        click_window_control('close')

        # Check that the deleted page is not auto-completed in the URL bar.
        select_location_bar()
        paste('http://127.0.0.1:2000/m')

        expected_4 = wait_vanish(mozilla_autocomplete.similar(0.9), 10)
        assert expected_4, 'Mozilla page is not auto-completed in URL bar.'
