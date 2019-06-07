# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Firefox can be set to always restore sessions on start',
        test_case_id='114844',
        test_suite_id='68',
        locales=Locales.ENGLISH
    )
    def run(self, firefox):
        restore_previous_session_checked_pattern = Pattern('restore_previous_session_checked.png')
        restore_previous_session_unchecked_pattern = Pattern('restore_previous_session_unchecked.png')
        iris_icon_title_pattern = Pattern('iris_tab.png')

        navigate('about:preferences')
        restore_previous_session_checkbox_available = exists(restore_previous_session_unchecked_pattern,
                                                             FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert restore_previous_session_checkbox_available, \
            'Page about:preferences is loaded. Checkbox \'Restore previous session\' is available'

        click(restore_previous_session_unchecked_pattern)
        checkbox_restore_previous_session_checked = exists(restore_previous_session_checked_pattern)
        assert checkbox_restore_previous_session_checked, '\'Restore previous session\' enabled.'

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)
        website_one_loaded = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert website_one_loaded, 'Page 1 successfully loaded, firefox logo found.'

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE_2)
        website_two_loaded = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert website_two_loaded, 'Page 2 successfully loaded, firefox logo found.'

        firefox.restart(image=iris_icon_title_pattern)

        next_tab()
        checkbox_restore_previous_session_checked = exists(restore_previous_session_checked_pattern.similar(0.6),
                                                           timeout=FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT)
        assert checkbox_restore_previous_session_checked, '\'Restore previous session\' checked.'

        click(restore_previous_session_checked_pattern)
        restore_previous_session_unchecked_exists = exists(restore_previous_session_unchecked_pattern)
        assert restore_previous_session_unchecked_exists, '\'Restore previous session\' is unchecked.'

        close_tab()
        website_one_loaded = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert website_one_loaded, 'Page 1 successfully loaded after restart.'

        next_tab()
        website_two_loaded = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert website_two_loaded, 'Page 2 successfully loaded after restart.'
