# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Check security.enterprise_roots.enabled set to true doesn\'t break TLS Client Authentication.',
        locale=[Locales.ENGLISH],
        test_case_id='225144',
        test_suite_id='3063'
    )
    def test_run(self, firefox):
        cdn77_logo_pattern = Pattern('cdn77_logo.png')
        cloudflare_logo_pattern = Pattern('cloudflare_logo.png')
        cdn77_support_button_pattern = Pattern('cdn77_support_button.png')
        cdn77_support_page_pattern = Pattern('cdn77_support_page.png')
        cloudflare_support_page_pattern = Pattern('cloudflare_support_page.png')
        download_button_pattern = Pattern('download_button.png')
        view_certificates_button_pattern = Pattern('view_certificates_button.png')
        certificate_manager_window_title_pattern = Pattern('certificate_manager_window_title.png')
        tls_certificate_name_pattern = Pattern('tls_certificate_name.png')
        tls_certificate_name_highlighted_pattern = Pattern('tls_certificate_name_highlighted.png')
        digicert_logo_pattern = Pattern('digicert_logo.png')
        cloudflare_support_button_pattern = Pattern('cloudflare_support_button.png')

        if OSHelper.is_windows():
            mouse_wheel_steps = 500
        elif OSHelper.is_linux():
            mouse_wheel_steps = 1
        else:
            mouse_wheel_steps = 5

        change_preference('security.enterprise_roots.enabled', 'True')

        navigate('https://www.digicert.com/digicert-root-certificates.htm')

        close_content_blocking_pop_up()

        restore_firefox_focus()
        assert exists(digicert_logo_pattern, Settings.DEFAULT_SITE_LOAD_TIMEOUT), 'DigiCert site is successfully opened'

        open_find()
        paste('DigiCert Assured ID TLS CA')
        assert exists(tls_certificate_name_highlighted_pattern), 'The TLS Certificate is available to download.'

        tls_certificate_location = find(tls_certificate_name_highlighted_pattern)
        tls_certificate_region = Region(tls_certificate_location.x, tls_certificate_location.y, Screen.SCREEN_WIDTH / 3,
                                        Screen.SCREEN_HEIGHT / 10)
        tls_certificate_region.click(download_button_pattern)
        assert exists(DownloadDialog.OK_BUTTON, 10), 'Certificate trust dialog opened.'

        click(DownloadDialog.OK_BUTTON)
        navigate('about:preferences#privacy')
        assert exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED), 'Preferences opened.'

        paste('Certificates')
        assert exists(view_certificates_button_pattern), 'View Certificates button displayed.'

        click(view_certificates_button_pattern)
        assert exists(certificate_manager_window_title_pattern), 'View Certificates window displayed.'

        certificate_manager_window_location = find(certificate_manager_window_title_pattern).below(200)
        Mouse().move(certificate_manager_window_location)
        assert scroll_until_pattern_found(tls_certificate_name_pattern, mouse_wheel_steps, 50), \
            'TLS Certificate is imported.'

        navigate('https://www.cdn77.com/')
        assert exists(cdn77_logo_pattern, Settings.DEFAULT_HEAVY_SITE_LOAD_TIMEOUT), \
            'CDN77 page is successfully downloaded.'
        assert exists(cdn77_support_button_pattern), 'CDN77 Support button is displayed.'

        click(cdn77_support_button_pattern)
        assert exists(cdn77_support_page_pattern, Settings.DEFAULT_HEAVY_SITE_LOAD_TIMEOUT), \
            'TLS client certificate authentication mechanism will not be broken. No errors occur.'

        navigate('https://www.cloudflare.com/')
        assert exists(cloudflare_logo_pattern, Settings.DEFAULT_HEAVY_SITE_LOAD_TIMEOUT), \
            'Cloudflare page is successfully downloaded.'
        assert exists(cloudflare_support_button_pattern), 'Cloudflare Support button is displayed.'

        click(cloudflare_support_button_pattern)
        assert exists(cloudflare_support_page_pattern, Settings.DEFAULT_HEAVY_SITE_LOAD_TIMEOUT), \
            'TLS client certificate authentication mechanism will not be broken. No errors occur.'
