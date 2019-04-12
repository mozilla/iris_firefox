# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'History is not remembered if reopening a Private window ' \
                    'from the dock (for a profile used only in private mode) '
        self.test_case_id = '120455'
        self.test_suite_id = '1826'
        self.locales = ['en-US']
        self.exclude = [Platform.WINDOWS, Platform.LINUX]

    def run(self):
        wiki_soap_history_icon_pattern = Pattern('wiki_soap_history_icon.png')
        top_sites_pattern = Pattern('top_sites.png')

        dock_region = Region(0, 0.8 * SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT)

        restart_firefox(self, self.browser.path, self.profile_path, '', args=['-private'],
                        image=PrivateWindow.private_window_pattern.similar(0.6))

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_label_exists = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, soap_label_exists, 'The page is successfully loaded.')

        close_window()
        confirm_close_multiple_tabs()

        window_closed = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, Settings.TINY_FIREFOX_TIMEOUT)
        assert_false(self, window_closed, 'The window is closed')

        firefox_icon_dock_exists = exists(Docker.FIREFOX_DOCKER_ICON, Settings.FIREFOX_TIMEOUT)
        assert_true(self, firefox_icon_dock_exists, 'The Firefox icon is still visible in the dock.')

        click(Docker.FIREFOX_DOCKER_ICON, in_region=dock_region)

        top_sites_item_exists = exists(top_sites_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, top_sites_item_exists, 'New window with new tab opened successfully.')

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_label_exists = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, soap_label_exists, 'The page is successfully loaded.')

        history_sidebar()

        type('soap')

        wiki_soap_history_icon_exists = exists(wiki_soap_history_icon_pattern, Settings.TINY_FIREFOX_TIMEOUT)
        assert_false(self, wiki_soap_history_icon_exists, 'The Recent History section is empty.')
