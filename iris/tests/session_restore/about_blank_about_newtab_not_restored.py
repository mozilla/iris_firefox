# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Bug 1323987 - about:blank and about:newtab aren\'t restored by Session Restore'
        self.test_case_id = '116003'
        self.test_suite_id = '68'
        self.locales = ['en-US']

    def run(self):
        new_tab()
        navigate('about:blank')

        top_sites_available = exists(Utils.TOP_SITES, Settings.FIREFOX_TIMEOUT)
        assert_true(self, top_sites_available, 'about:newtab available')

        new_tab()
        navigate('about:newtab')

        top_sites_available = exists(Utils.TOP_SITES, Settings.TINY_FIREFOX_TIMEOUT)
        assert_false(self, top_sites_available, 'about:blank available')

        restart_firefox(self, self.browser.path, self.profile_path, self.base_local_web_url)

        new_tab_not_highlighted = exists(Tabs.NEW_TAB_NOT_HIGHLIGHTED)
        assert_true(self, new_tab_not_highlighted, 'Not highlighted new tab is available')

        click(Tabs.NEW_TAB_NOT_HIGHLIGHTED, 1)

        top_sites_available = exists(Utils.TOP_SITES, Settings.TINY_FIREFOX_TIMEOUT)

        if top_sites_available:
            assert_true(self, top_sites_available, 'about:newtab available')
        else:
            assert_false(self, top_sites_available, 'about:blank available')

        new_tab_not_highlighted = exists(Tabs.NEW_TAB_NOT_HIGHLIGHTED)
        assert_true(self, new_tab_not_highlighted, 'new_tab_not_highlighted')

        click(Tabs.NEW_TAB_NOT_HIGHLIGHTED, 1)

        top_sites_available = exists(Utils.TOP_SITES, Settings.TINY_FIREFOX_TIMEOUT)

        if top_sites_available:
            assert_true(self, top_sites_available, 'about:newtab available')
        else:
            assert_false(self, top_sites_available, 'about:blank available')
