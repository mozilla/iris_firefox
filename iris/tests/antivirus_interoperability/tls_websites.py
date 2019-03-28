# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = "Websites using TLS 1.3 "
        self.test_case_id = "217857"
        self.test_suite_id = "3036"
        self.locale = ["en-US"]

    def run(self):
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

        cloudflare_logo_displayed = exists(cloudflare_logo_pattern, Settings.HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, cloudflare_logo_displayed, 'Cloudflare page is successfully downloaded')

        click(LocationBar.IDENTITY_ICON)

        cloudflare_show_connection_details_exists = exists(show_connection_details_button_pattern,
                                                           Settings.FIREFOX_TIMEOUT)
        assert_true(self, cloudflare_show_connection_details_exists, 'Show Connection Details button displayed')

        click(show_connection_details_button_pattern)

        cloudflare_more_info_button_exists = exists(more_information_button_pattern, Settings.FIREFOX_TIMEOUT)

        assert_true(self, cloudflare_more_info_button_exists, 'More information button displayed')

        click(more_information_button_pattern)

        cloudflare_page_info_opened = exists(page_info_window_pattern)
        assert_true(self, cloudflare_page_info_opened, 'Cloudflare page info window is opened')

        cloudflare_tls_check_pattern_matching = exists(tls_check_pattern)
        assert_true(self, cloudflare_tls_check_pattern_matching, 'The Technical Details section states that the '
                                                                 'connection is encrypted via TLS 1.3')

        close_window_control('auxiliary')

        cloudflare_support_button_exists = exists(cloudflare_support_button_pattern)
        assert_true(self, cloudflare_support_button_exists, 'Cloudflare support login button exists')

        click(cloudflare_support_button_pattern)

        cloudflare_support_page_displayed = exists(cloudflare_support_page_pattern, Settings.HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, cloudflare_support_page_displayed, 'There are no issues, crashes while navigating'
                                                             'on the website')

        navigate('https://www.theregister.co.uk/')

        theregister_logo_displayed = exists(theregister_logo_pattern, Settings.HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, theregister_logo_displayed, 'The Register page is successfully downloaded')

        click(LocationBar.IDENTITY_ICON)
        theregister_show_connection_details_exists = exists(show_connection_details_button_pattern,
                                                            Settings.FIREFOX_TIMEOUT)
        assert_true(self, theregister_show_connection_details_exists, 'Show Connection Details button displayed')

        click(show_connection_details_button_pattern)

        theregister_more_info_button_exists = exists(more_information_button_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, theregister_more_info_button_exists, 'More information button displayed')

        click(more_information_button_pattern)

        the_register_logo_displayed_page_info_opened = exists(page_info_window_pattern)
        assert_true(self, the_register_logo_displayed_page_info_opened, 'The Register page info window is opened')

        the_register_tls_check_pattern_matching = exists(tls_check_pattern)
        assert_true(self, the_register_tls_check_pattern_matching, 'The Technical Details section states that the '
                                                                   'connection is encrypted via TLS 1.3')

        close_window_control('auxiliary')

        the_register_log_in_button_exists = exists(the_regiter_log_in_button_pattern)
        assert_true(self, the_register_log_in_button_exists, 'The Register Log In button exists')

        click(the_regiter_log_in_button_pattern)

        the_register_log_in_page_displayed = exists(the_register_log_in_page_pattern, Settings.HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, the_register_log_in_page_displayed, 'There are no issues, crashes while navigating'
                                                              'on the website')

        navigate('https://www.cdn77.com/')

        cdn77_logo_displayed = exists(cdn77_logo_pattern, Settings.HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, cdn77_logo_displayed, 'CDN77 page is successfully downloaded')

        click(LocationBar.IDENTITY_ICON)

        cdn77_show_connection_details_exists = exists(show_connection_details_button_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, cdn77_show_connection_details_exists, 'Show Connection Details button displayed')

        click(show_connection_details_button_pattern)

        cdn77_more_info_button_exists = exists(more_information_button_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, cdn77_more_info_button_exists, 'More information button displayed')

        click(more_information_button_pattern)

        cdn77_logo_displayed_page_info_opened = exists(page_info_window_pattern)
        assert_true(self, cdn77_logo_displayed_page_info_opened, 'CDN77 page info window is opened')

        cdn77_tls_check_pattern_matching = exists(tls_check_pattern)
        assert_true(self, cdn77_tls_check_pattern_matching, 'The Technical Details section states that the '
                                                            'connection is encrypted via TLS 1.3')

        close_window_control('auxiliary')

        cdn77_support_button_exists = exists(cdn77_support_button_pattern)
        assert_true(self, cdn77_support_button_exists, 'The Register Log In button exists')

        click(cdn77_support_button_pattern)

        cdn77_support_page_displayed = exists(cdn77_support_page_pattern, Settings.HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, cdn77_support_page_displayed, 'There are no issues, crashes while navigating on the website')
