# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = " Check security.enterprise_roots.enabled set to true doesn't break TLS Client Authentication."
        self.test_case_id = "225144"
        self.test_suite_id = "3063"
        self.locale = ["en-US"]

    def run(self):
        cdn77_logo_pattern = Pattern('cdn77_logo.png')
        cloudflare_logo_pattern = Pattern('cloudflare_logo.png')
        cdn77_support_button_pattern = Pattern('cdn77_support_button.png').similar(0.65)
        cdn77_support_page_pattern = Pattern('cdn77_support_page.png')
        cloudflare_support_page_pattern = Pattern('cloudflare_support_page.png')
        download_button_pattern = Pattern('download_button.png')
        view_certificates_button_pattern = Pattern('view_certificates_button.png')
        certificate_manager_window_title_pattern = Pattern('certificate_manager_window_title.png')
        tls_certificate_name_pattern = Pattern('tls_certificate_name.png')
        tls_certificate_name_highlighted_pattern = Pattern('tls_certificate_name_highlighted.png')
        digicert_logo_pattern = Pattern('digicert_logo.png')
        cloudflare_support_button_pattern = Pattern('cloudflare_support_button.png')

        if Settings.is_windows():
            mouse_wheel_steps = 500
        elif Settings.is_linux():
            mouse_wheel_steps = 1
        else:
            mouse_wheel_steps = 5

        change_preference('security.enterprise_roots.enabled', 'True')

        navigate('https://www.digicert.com/digicert-root-certificates.htm')

        restore_firefox_focus()

        digicert_site_opened = exists(digicert_logo_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, digicert_site_opened, 'DigiCert site is successfully opened')

        open_find()

        paste('DigiCert Assured ID TLS CA')

        tls_certificate_exists = exists(tls_certificate_name_highlighted_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, tls_certificate_exists, 'The TLS Certificate is available to download')

        tls_certificate_location = find(tls_certificate_name_highlighted_pattern)
        tls_certificate_region = Region(tls_certificate_location.x, tls_certificate_location.y, SCREEN_WIDTH / 3,
                                        SCREEN_HEIGHT / 10)
        click(download_button_pattern, in_region=tls_certificate_region)

        certificate_trust_dialog_opened = exists(DownloadDialog.OK_BUTTON, Settings.FIREFOX_TIMEOUT)
        assert_true(self, certificate_trust_dialog_opened, 'Certificate trust dialog opened')

        click(DownloadDialog.OK_BUTTON)

        navigate('about:preferences#privacy')

        preferences_privacy_opened = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED,
                                            Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, preferences_privacy_opened, 'Preferences opened')

        paste('Certificates')

        view_certificates_button_exists = exists(view_certificates_button_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, view_certificates_button_exists, 'View Certificates button displayed')

        click(view_certificates_button_pattern)

        certificate_manager_window_opened = exists(certificate_manager_window_title_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, certificate_manager_window_opened, 'View Certificates window displayed')

        certificate_manager_window_location = find(certificate_manager_window_title_pattern).below(200)
        hover(certificate_manager_window_location)

        tls_certificate_is_imported = scroll_until_pattern_found(tls_certificate_name_pattern, scroll,
                                                                 (-mouse_wheel_steps,), 50)
        assert_true(self, tls_certificate_is_imported, 'TLS Certificate is imported')

        navigate('https://www.cdn77.com/')

        cdn77_logo_displayed = exists(cdn77_logo_pattern, Settings.HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, cdn77_logo_displayed, 'CDN77 page is successfully downloaded')

        cdn77_support_button_displayed = exists(cdn77_support_button_pattern)
        assert_true(self, cdn77_support_button_displayed, 'CDN77 Support button is displayed')

        click(cdn77_support_button_pattern)

        cdn77_support_page_displayed = exists(cdn77_support_page_pattern, Settings.HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, cdn77_support_page_displayed, 'TLS client certificate authentication mechanism will not '
                                                        'be broken. No errors occur')

        navigate('https://www.cloudflare.com/')

        cloudflare_logo_displayed = exists(cloudflare_logo_pattern, Settings.HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, cloudflare_logo_displayed, 'Cloudflare page is successfully downloaded')

        cloudflare_support_button_displayed = exists(cloudflare_support_button_pattern)
        assert_true(self, cloudflare_support_button_displayed, 'Cloudflare Support button is displayed')

        click(cloudflare_support_button_pattern)

        cloudflare_support_page_displayed = exists(cloudflare_support_page_pattern, Settings.HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, cloudflare_support_page_displayed, 'TLS client certificate authentication mechanism will not '
                                                             'be broken. No errors occur')
