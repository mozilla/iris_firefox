# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Check security.enterprise_roots.enabled set to true doesn\'t break TLS Client Authentication.',
        locale=['en-US'],
        test_case_id='225144',
        test_suite_id='3063'
    )
    def run(self, firefox):
        cdn77_logo_pattern = Pattern('cdn77_logo.png')
        cloudflare_logo_pattern = Pattern('cloudflare_logo.png')
        cdn77_support_page_pattern = Pattern('cdn77_support_page.png')
        cloudflare_support_page_pattern = Pattern('cloudflare_support_page.png')
        download_button_pattern = Pattern('download_button.png').similar(.7)
        view_certificates_button_pattern = Pattern('view_certificates_button.png')
        certificate_manager_window_title_pattern = Pattern('certificate_manager_window_title.png')
        tls_certificate_name_pattern_1 = Pattern('tls_certificate_name_1.png')
        tls_certificate_name_pattern = Pattern('tls_certificate_name.png')
        tls_certificate_name_highlighted_pattern = Pattern('tls_certificate_name_highlighted.png')
        digicert_logo_pattern = Pattern('digicert_logo.png')
        cloudflare_support_button_pattern = Pattern('cloudflare_support_button.png')
        cdn77_tab_logo_pattern = Pattern('cdn77_tab_logo.png')

        home_width, home_height = NavBar.HOME_BUTTON.get_size()
        tabs_region = Region(0, 0, Screen.SCREEN_WIDTH, home_height * 4)

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

        tls_certificate_found_grey = scroll_until_pattern_found(tls_certificate_name_pattern,
                                                                scroll, (-mouse_wheel_steps,), 50,
                                                                timeout=FirefoxSettings.TINY_FIREFOX_TIMEOUT//2)
        if tls_certificate_found_grey:
            assert tls_certificate_found_grey, 'TLS Certificate is imported.'
        else:
            tls_certificate_found_white = scroll_until_pattern_found(tls_certificate_name_pattern_1,
                                                                     scroll, (mouse_wheel_steps,), 50,
                                                                     timeout=FirefoxSettings.TINY_FIREFOX_TIMEOUT//2)
            assert tls_certificate_found_white, 'TLS Certificate is imported.'

        navigate('https://www.cdn77.com/')
        assert exists(cdn77_tab_logo_pattern, Settings.DEFAULT_HEAVY_SITE_LOAD_TIMEOUT, tabs_region), \
            'CDN77 page is successfully downloaded.'

        assert exists(cdn77_logo_pattern, Settings.DEFAULT_HEAVY_SITE_LOAD_TIMEOUT), \
            'CDN77 page is successfully downloaded.'

        cdn_button_location = find(cdn77_logo_pattern)
        cdn_width, cdn_height = cdn77_logo_pattern.get_size()
        cdn_region = Region(cdn_button_location.x, cdn_button_location.y, Screen.SCREEN_WIDTH*0.7, cdn_height)

        assert exists("Support", FirefoxSettings.FIREFOX_TIMEOUT, region=cdn_region), \
            'CDN77 Support button is displayed.'

        click("Support", region=cdn_region)

        assert exists(cdn77_support_page_pattern, Settings.DEFAULT_HEAVY_SITE_LOAD_TIMEOUT), \
            'TLS client certificate authentication mechanism will not be broken. No errors occur.'

        navigate('https://www.cloudflare.com/')

        assert exists(cloudflare_logo_pattern, Settings.DEFAULT_HEAVY_SITE_LOAD_TIMEOUT, tabs_region), \
            'Cloudflare page is successfully downloaded.'
        assert exists(cloudflare_support_button_pattern.similar(.7)), 'Cloudflare Support button is displayed.'

        click(cloudflare_support_button_pattern)
        assert exists(cloudflare_support_page_pattern, Settings.DEFAULT_HEAVY_SITE_LOAD_TIMEOUT), \
            'TLS client certificate authentication mechanism will not be broken. No errors occur.'
