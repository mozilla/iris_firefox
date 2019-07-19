# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bug 1345569 - User can report deceptive site when visiting Open any webpage',
        test_case_id='171423',
        test_suite_id='69',
        locale=['en-US'],
        profile=Profiles.BRAND_NEW
    )
    def run(self, firefox):
        google_logo_pattern = Pattern('google_logo.png')
        url_field_pattern = Pattern('url_field.png')

        navigate(LocalWeb.POCKET_TEST_SITE)

        test_site_opened = exists(LocalWeb.POCKET_IMAGE, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert test_site_opened, 'Test site opened'

        click_hamburger_menu_option('Help')

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        report_deceptive_site_option_exists = exists('Report', FirefoxSettings.FIREFOX_TIMEOUT,
                                                     Screen.RIGHT_THIRD)
        assert report_deceptive_site_option_exists, '"Report Deceptive Site..." option exists'

        click('Report Deceptive Site', region=Screen.RIGHT_THIRD)

        report_web_page_loaded = exists(google_logo_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert report_web_page_loaded, 'Report Web Forgery page is loaded.'

        url_field_found = exists(url_field_pattern, FirefoxSettings.FIREFOX_TIMEOUT, Screen.MIDDLE_THIRD_VERTICAL)
        assert url_field_found, 'URL field was found'

        click(url_field_pattern, region=Screen.MIDDLE_THIRD_VERTICAL)

        edit_copy()
        filled_url = get_clipboard()
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/3)
        assert filled_url in LocalWeb.POCKET_TEST_SITE, "The deceptive URL is auto filled."

        # Possibility reporting the phishing website doesn't checked because of re-captcha
