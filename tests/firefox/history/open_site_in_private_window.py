# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Open a website in a private window and then check it is not displayed in the Recent History list.',
        locale=['en-US'],
        test_case_id='118806',
        test_suite_id='2000',
        profile=Profiles.BRAND_NEW
    )
    def run(self, firefox):
        recent_history_default_pattern = Pattern('recent_history_default.png')

        # Open a website in a new private window.
        new_private_window()

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        test_site_loaded = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert test_site_loaded is True, 'Mozilla page loaded successfully.'

        # Check that the previously opened page is not displayed in the Recent History list.
        library_button_exists = exists(NavBar.LIBRARY_MENU)
        assert library_button_exists is True, 'Library button exists'

        click(NavBar.LIBRARY_MENU)

        history_button_exists = exists(LibraryMenu.HISTORY_BUTTON, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert history_button_exists is True, 'History button exists'

        click(LibraryMenu.HISTORY_BUTTON)

        page_not_displayed = exists(recent_history_default_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert page_not_displayed is True, 'Mozilla page is not displayed in the History list.'
