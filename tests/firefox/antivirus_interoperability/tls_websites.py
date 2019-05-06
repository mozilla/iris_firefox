# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='ebsites using TLS 1.3.',
        locale=[Locales.ENGLISH],
        test_case_id='217857',
        test_suite_id='3063'
    )
    def run(self, firefox):
        page_info_window_pattern = Pattern('technical_details.png')
        tls_check_pattern = Pattern('tls_check.png')
        show_connection_details_button_pattern = Pattern('show_connection_details_button.png')
        more_information_button_pattern = Pattern('more_information_button.png')
        cloudflare_logo_pattern = Pattern('cloudflare_logo.png')
        theregister_logo_pattern = Pattern('theregister_logo.png')
        cdn77_logo_pattern = Pattern('cdn77_logo.png')
        cloudflare_support_page_pattern = Pattern('cloudflare_support_page.png')
        cloudflare_support_button_pattern = Pattern('cloudflare_support_button.png')
        the_regiter_log_in_button_pattern = Pattern('the_regiter_log_in_button.png')
        the_register_log_in_page_pattern = Pattern('the_register_log_in_page.png')
        cdn77_support_button_pattern = Pattern('cdn77_support_button.png').similar(.6)
        cdn77_support_page_pattern = Pattern('cdn77_support_page.png')

        navigate('https://www.cloudflare.com/')
        assert exists(cloudflare_logo_pattern, Settings.DEFAULT_HEAVY_SITE_LOAD_TIMEOUT), \
            'Cloudflare page is successfully downloaded.'

        click(LocationBar.IDENTITY_ICON)
        assert exists(show_connection_details_button_pattern, 10), 'Show Connection Details button displayed.'

        click(show_connection_details_button_pattern, 10)
        assert exists(more_information_button_pattern), 'More information button displayed.'

        click(more_information_button_pattern)
        assert exists(page_info_window_pattern), 'Cloudflare page info window is opened.'
        assert exists(tls_check_pattern), \
            'The Technical Details section states that the connection is encrypted via TLS 1.3.'

        close_window_control('auxiliary')
        assert exists(cloudflare_support_button_pattern), 'Cloudflare support login button exists.'

        click(cloudflare_support_button_pattern)
        assert exists(cloudflare_support_page_pattern, Settings.DEFAULT_HEAVY_SITE_LOAD_TIMEOUT), \
            'There are no issues, crashes while navigating on the website.'

        navigate('https://www.theregister.co.uk/')
        assert exists(theregister_logo_pattern, Settings.DEFAULT_HEAVY_SITE_LOAD_TIMEOUT), \
            'The Register page is successfully downloaded.'

        click(LocationBar.IDENTITY_ICON)
        assert exists(show_connection_details_button_pattern, 10), 'Show Connection Details button displayed.'

        click(show_connection_details_button_pattern)
        assert exists(more_information_button_pattern, 10), 'More information button displayed.'

        click(more_information_button_pattern)
        assert exists(page_info_window_pattern), 'The Register page info window is opened.'
        assert exists(tls_check_pattern), \
            'The Technical Details section states that the connection is encrypted via TLS 1.3.'

        close_window_control('auxiliary')
        assert exists(the_regiter_log_in_button_pattern), 'The Register Log In button exists.'

        click(the_regiter_log_in_button_pattern)
        assert exists(the_register_log_in_page_pattern, Settings.DEFAULT_HEAVY_SITE_LOAD_TIMEOUT), \
            'There are no issues, crashes while navigating on the website.'

        navigate('https://www.cdn77.com/')
        assert exists(cdn77_logo_pattern, Settings.DEFAULT_HEAVY_SITE_LOAD_TIMEOUT), \
            'CDN77 page is successfully downloaded.'

        click(LocationBar.IDENTITY_ICON)
        assert exists(show_connection_details_button_pattern, Settings.DEFAULT_FIREFOX_TIMEOUT), \
            'Show Connection Details button displayed.'

        click(show_connection_details_button_pattern)
        assert exists(more_information_button_pattern, Settings.DEFAULT_FIREFOX_TIMEOUT), \
            'More information button displayed.'

        click(more_information_button_pattern)
        assert exists(page_info_window_pattern), 'CDN77 page info window is opened.'
        assert exists(tls_check_pattern), \
            'The Technical Details section states that the connection is encrypted via TLS 1.3.'

        close_window_control('auxiliary')
        assert exists(cdn77_support_button_pattern), 'The Register Log In button exists.'

        click(cdn77_support_button_pattern)
        assert exists(cdn77_support_page_pattern, Settings.DEFAULT_HEAVY_SITE_LOAD_TIMEOUT), \
            'There are no issues, crashes while navigating on the website.'
