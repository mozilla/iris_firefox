# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='ebsites using TLS 1.3.',
        locale=['en-US'],
        test_case_id='217857',
        test_suite_id='3063'
    )
    def run(self, firefox):
        page_info_window_pattern = Pattern('technical_details.png')
        tls_check_pattern = Pattern('tls_check.png').similar(0.7)
        show_connection_details_button_pattern = Pattern('show_connection_details_button.png')
        more_information_button_pattern = Pattern('more_information_button.png')
        cloudflare_logo_pattern = Pattern('cloudflare_logo.png')
        theregister_logo_pattern = Pattern('theregister_logo.png')
        cdn77_logo_pattern = Pattern('cdn77_logo.png')
        cloudflare_support_page_pattern = Pattern('cloudflare_support_page.png')
        cloudflare_support_button_pattern = Pattern('cloudflare_support_button.png')
        the_regiter_log_in_button_pattern = Pattern('the_regiter_log_in_button.png').similar(0.6)
        the_register_log_in_page_pattern = Pattern('the_register_log_in_page.png').similar(0.6)
        cdn77_support_page_pattern = Pattern('cdn77_support_page.png')

        navigate('https://www.cloudflare.com/')
        assert exists(cloudflare_logo_pattern, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT), \
            'Cloudflare page is successfully downloaded.'

        click(LocationBar.IDENTITY_ICON)
        assert exists(show_connection_details_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT), \
            'Show Connection Details button displayed.'

        click(show_connection_details_button_pattern)

        assert exists(more_information_button_pattern), 'More information button displayed.'

        click(more_information_button_pattern)

        assert exists(page_info_window_pattern), 'Cloudflare page info window is opened.'

        assert exists(tls_check_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT), \
            'The Technical Details section states that the connection is encrypted via TLS 1.3.'

        close_window_control('auxiliary')

        assert exists(cloudflare_support_button_pattern), 'Cloudflare support login button exists.'

        click(cloudflare_support_button_pattern)

        assert exists(cloudflare_support_page_pattern, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT), \
            'There are no issues, crashes while navigating on the website.'

        navigate('https://www.theregister.co.uk/')

        assert exists(theregister_logo_pattern, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT), \
            'The Register page is successfully downloaded.'

        click(LocationBar.IDENTITY_ICON)

        assert exists(show_connection_details_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT),\
            'Show Connection Details button displayed.'

        click(show_connection_details_button_pattern)

        assert exists(more_information_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT), \
            'More information button displayed.'

        click(more_information_button_pattern)

        assert exists(page_info_window_pattern, FirefoxSettings.FIREFOX_TIMEOUT), 'The Register page info window is opened.'

        assert exists(tls_check_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT), \
            'The Technical Details section states that the connection is encrypted via TLS 1.3.'

        close_window_control('auxiliary')

        assert exists(the_regiter_log_in_button_pattern), 'The Register Log In button exists.'

        click(the_regiter_log_in_button_pattern)

        assert exists(the_register_log_in_page_pattern, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT), \
            'There are no issues, crashes while navigating on the website.'

        navigate('https://www.cdn77.com/')

        cdn_logo_region = Screen().top_half().left_third().top_half()

        assert exists(cdn77_logo_pattern, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT, cdn_logo_region), \
            'CDN77 page is successfully downloaded.'

        cdn_button_location = find(cdn77_logo_pattern, region=cdn_logo_region)
        cdn_width, cdn_height = cdn77_logo_pattern.get_size()
        cdn_region = Rectangle(cdn_button_location.x, cdn_button_location.y, Screen.SCREEN_WIDTH*0.7, cdn_height)

        click(LocationBar.IDENTITY_ICON)

        assert exists(show_connection_details_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT), \
            'Show Connection Details button displayed.'

        click(show_connection_details_button_pattern)

        assert exists(more_information_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT), \
            'More information button displayed.'

        click(more_information_button_pattern)
        assert exists(page_info_window_pattern, FirefoxSettings.FIREFOX_TIMEOUT), 'CDN77 page info window is opened.'
        assert exists(tls_check_pattern, FirefoxSettings.FIREFOX_TIMEOUT), \
            'The Technical Details section states that the connection is encrypted via TLS 1.3.'

        close_window_control('auxiliary')

        assert exists("Support", FirefoxSettings.FIREFOX_TIMEOUT, region=cdn_region), \
            'CDN77 Support button is displayed.'

        click("Support", region=cdn_region)

        assert exists(cdn77_support_page_pattern, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT), \
            'TLS client certificate authentication mechanism will not be broken. No errors occur.'
