# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Firefox can be set to always restore sessions on start'
        self.test_case_id = '114844'
        self.test_suite_id = '68'
        self.locales = ['en-US']

    def run(self):
        url_first = LocalWeb.FIREFOX_TEST_SITE
        url_second = LocalWeb.FIREFOX_TEST_SITE_2
        restore_previous_session_checked_pattern = Pattern('restore_previous_session_checked.png')
        restore_previous_session_unchecked_pattern = Pattern('restore_previous_session_unchecked.png')
        iris_icon_title_pattern = Pattern('iris_tab.png')

        navigate('about:preferences')
        restore_previous_session_checkbox_available = exists(restore_previous_session_unchecked_pattern, 20)
        assert_true(self, restore_previous_session_checkbox_available,
                    'Page about:preferences is loaded. Checkbox "Restore previous session" is available')

        click(restore_previous_session_unchecked_pattern)
        checkbox_restore_previous_session_checked = exists(restore_previous_session_checked_pattern)
        assert_true(self, checkbox_restore_previous_session_checked, '"Restore previous session" enabled.')

        new_tab()
        navigate(url_first)
        website_one_loaded = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, website_one_loaded, 'Page 1 successfully loaded, firefox logo found.')

        new_tab()
        navigate(url_second)
        website_two_loaded = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, website_two_loaded, 'Page 2 successfully loaded, firefox logo found.')

        restart_firefox(self,
                        self.browser.path,
                        self.profile_path,
                        self.base_local_web_url,
                        image=iris_icon_title_pattern)

        next_tab()
        checkbox_restore_previous_session_checked = exists(restore_previous_session_checked_pattern.similar(0.6),
                                                           timeout=DEFAULT_HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, checkbox_restore_previous_session_checked, '"Restore previous session" checked.')

        click(restore_previous_session_checked_pattern)
        restore_previous_session_unchecked_exists = exists(restore_previous_session_unchecked_pattern, 20)
        assert_true(self, restore_previous_session_unchecked_exists, '"Restore previous session" is unchecked.')

        close_tab()
        website_one_loaded = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, website_one_loaded, 'Page 1 successfully loaded after restart.')

        next_tab()
        website_two_loaded = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, website_two_loaded, 'Page 2 successfully loaded after restart.')
