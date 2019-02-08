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
        facebook_logo_pattern = Pattern('facebook_logo.png')
        page_info_window_pattern = Pattern('technical_details.png')
        tls_check_pattern = Pattern('tls_check.png')
        show_connection_details_button_pattern = Pattern('show_connection_details_button.png')
        more_information_button_pattern = Pattern('more_information_button.png')
        cloudflare_logo_pattern = Pattern('cloudflare_logo.png')
        theregister_logo_pattern = Pattern('theregister_logo.png')
        cdn77_logo_pattern = Pattern('cdn77_logo.png')
        facebook_create_new_account_button_pattern = Pattern('facebook_create_new_account_button.png')
        facebook_login_button_pattern = Pattern('facebook_login_button.png')
        cloudflare_support_page_pattern = Pattern('cloudflare_support_page.png')
        cloudflare_support_button_pattern = Pattern('cloudflare_support_button.png')
        the_regiter_log_in_button_pattern = Pattern('the_regiter_log_in_button.png')
        the_register_log_in_page_pattern = Pattern('the_register_log_in_page.png')
        cdn77_support_button_pattern = Pattern('cdn77_support_button.png').similar(.6)
        cdn77_support_page_pattern = Pattern('cdn77_support_page.png')

        navigate('https://www.facebook.com/')

        close_content_blocking_pop_up()

        facebook_logo_displayed = exists(facebook_logo_pattern, DEFAULT_HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, facebook_logo_displayed, 'Facebook page is successfully downloaded')

        click(LocationBar.IDENTITY_ICON)
        time.sleep(DEFAULT_UI_DELAY)
        click(show_connection_details_button_pattern)
        time.sleep(DEFAULT_UI_DELAY)
        click(more_information_button_pattern)

        facebook_page_info_opened = exists(page_info_window_pattern)
        assert_true(self, facebook_page_info_opened, 'Facebook page info window is opened')

        facebook_tls_check_pattern_matching = exists(tls_check_pattern)
        assert_true(self, facebook_tls_check_pattern_matching, 'The Technical Details section states that the '
                                                               'connection is encrypted via TLS 1.3')

        close_window_control('auxiliary')

        facebook_login_button_exists = exists(facebook_login_button_pattern)
        assert_true(self, facebook_login_button_exists, 'Facebook login button exists')

        click(facebook_login_button_pattern)

        facebook_create_new_account_button_exists = exists(facebook_create_new_account_button_pattern,
                                                           DEFAULT_HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, facebook_create_new_account_button_exists, 'There are no issues, crashes while navigating'
                                                                     'on the website')

        navigate('https://www.cloudflare.com/')

        cloudflare_logo_displayed = exists(cloudflare_logo_pattern, DEFAULT_HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, cloudflare_logo_displayed, 'Cloudflare page is successfully downloaded')

        click(LocationBar.IDENTITY_ICON)
        time.sleep(DEFAULT_UI_DELAY)
        click(show_connection_details_button_pattern)
        time.sleep(DEFAULT_UI_DELAY)
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

        cloudflare_support_page_displayed = exists(cloudflare_support_page_pattern, DEFAULT_HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, cloudflare_support_page_displayed, 'There are no issues, crashes while navigating'
                                                             'on the website')

        navigate('https://www.theregister.co.uk/')

        theregister_logo_displayed = exists(theregister_logo_pattern, DEFAULT_HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, theregister_logo_displayed, 'The Register page is successfully downloaded')

        click(LocationBar.IDENTITY_ICON)
        time.sleep(DEFAULT_UI_DELAY)
        click(show_connection_details_button_pattern)
        time.sleep(DEFAULT_UI_DELAY)
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

        the_register_log_in_page_displayed = exists(the_register_log_in_page_pattern, DEFAULT_HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, the_register_log_in_page_displayed, 'There are no issues, crashes while navigating'
                                                              'on the website')

        navigate('https://www.cdn77.com/')

        cdn77_logo_displayed = exists(cdn77_logo_pattern, DEFAULT_HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, cdn77_logo_displayed, 'CDN77 page is successfully downloaded')

        click(LocationBar.IDENTITY_ICON)
        time.sleep(DEFAULT_UI_DELAY)
        click(show_connection_details_button_pattern)
        time.sleep(DEFAULT_UI_DELAY)
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

        cdn77_support_page_displayed = exists(cdn77_support_page_pattern, DEFAULT_HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, cdn77_support_page_displayed, 'There are no issues, crashes while navigating on the website')
