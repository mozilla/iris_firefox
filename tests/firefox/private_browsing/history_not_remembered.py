# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='History is not remembered if reopening a Private window '
                    'from the dock (for a profile used only in private mode) ',
        test_case_id='120455',
        test_suite_id='1826',
        locales=['en-US'],
        exclude=[OSPlatform.WINDOWS, OSPlatform.LINUX],
        # blocked_by={'id': 'issue_3220', 'platform': OSPlatform.ALL}
    )
    def run(self, firefox):
        wiki_soap_history_icon_pattern = Pattern('wiki_soap_history_icon.png')
        top_sites_pattern = Pattern('top_sites.png')

        dock_region = Region(0, int(0.8 * Screen.SCREEN_HEIGHT), Screen.SCREEN_WIDTH, int(0.2 * Screen.SCREEN_HEIGHT))

        firefox.restart()

        private_window_opened = exists(PrivateWindow.private_window_pattern.similar(0.6))
        assert private_window_opened, "Private window loaded."

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_label_exists = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert soap_label_exists is True, 'The page is successfully loaded.'

        close_window()
        confirm_close_multiple_tabs()

        window_closed = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        assert window_closed is False, 'The window is closed'

        firefox_icon_dock_exists = exists(Docker.FIREFOX_DOCKER_ICON, FirefoxSettings.FIREFOX_TIMEOUT)
        assert firefox_icon_dock_exists is True, 'The Firefox icon is still visible in the dock.'

        click(Docker.FIREFOX_DOCKER_ICON, FirefoxSettings.TINY_FIREFOX_TIMEOUT, region=dock_region)

        top_sites_item_exists = exists(top_sites_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert top_sites_item_exists is True, 'New window with new tab opened successfully.'

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_label_exists = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, FirefoxSettings.FIREFOX_TIMEOUT)
        assert soap_label_exists is True, 'The page is successfully loaded.'

        history_sidebar()

        type('soap')

        wiki_soap_history_icon_exists = exists(wiki_soap_history_icon_pattern, FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        assert wiki_soap_history_icon_exists is False, 'The Recent History section is empty.'
