# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='The recently closed tabs can be restored from the context menu',
        test_case_id='117049',
        test_suite_id='68',
        locales=Locales.ENGLISH
    )
    def run(self, firefox):
        test_urls = [LocalWeb.FIREFOX_TEST_SITE, LocalWeb.FOCUS_TEST_SITE]
        logo_patterns = [LocalWeb.FIREFOX_LOGO, LocalWeb.FOCUS_LOGO]
        firefox_local_tab_pattern = Pattern('firefox_local_tab.png')
        undo_close_tab_pattern = Pattern('undo_close_tab.png')

        new_tab()
        navigate(test_urls[0])
        first_website_loaded = exists(logo_patterns[0], FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert first_website_loaded, 'First tab is successfully loaded.'

        new_tab()
        navigate(test_urls[1])
        second_website_loaded = exists(logo_patterns[1], FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert second_website_loaded, 'Second tab is successfully loaded.'

        close_tab()
        try:
            second_tab_closed = wait_vanish(logo_patterns[1])
            assert second_tab_closed, 'Second tab successfully closed.'
        except FindError:
            raise FindError('Second tab is still open')
        first_tab_is_active = exists(firefox_local_tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert first_tab_is_active, 'First tab is active.'

        right_click(firefox_local_tab_pattern)
        context_menu_exists = exists(undo_close_tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert context_menu_exists, 'Undo Close Tab option exists.'

        click(undo_close_tab_pattern)
        second_website_loaded = exists(logo_patterns[1], FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert second_website_loaded, 'The previously closed tab is reopened.'
