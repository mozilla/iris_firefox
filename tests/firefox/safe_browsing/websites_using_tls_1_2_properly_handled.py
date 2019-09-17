# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Websites using the TLS v1.2 protocol are properly handled',
        test_case_id='192739',
        test_suite_id='69',
        locale=['en-US'],
    )
    def run(self, firefox):
        bad_ssl_green_logo_pattern = Pattern('bad_ssl_green_logo.png')
        show_connection_details_button_pattern = Pattern('show_connection_details_button.png')
        more_information_button_pattern = Pattern('more_information_button.png')
        tls_connection_encrypted_message_pattern = Pattern('tls_1_2_connection_encrypted_message.png')

        navigate('https://tls-v1-2.badssl.com:1012/')

        bad_ssl_page_loaded = exists(bad_ssl_green_logo_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert bad_ssl_page_loaded, 'Bad SSL page sucessfully loaded'

        connection_is_secure = exists(LocationBar.SECURE_CONNECTION_LOCK, FirefoxSettings.FIREFOX_TIMEOUT)
        assert connection_is_secure, 'The connection is secure.'

        edit_select_all()

        edit_copy()

        text_displayed = get_clipboard().replace('\n', '').replace('\r', '')
        assert text_displayed in 'tls-v1-2.badssl.com', 'The URL is properly loaded and green background page is ' \
                                                        'displayed, containing a string saying: tls-v1-2.badssl.com'

        click(LocationBar.SECURE_CONNECTION_LOCK)

        show_connection_details_button_displayed = exists(show_connection_details_button_pattern,
                                                          FirefoxSettings.FIREFOX_TIMEOUT)
        assert show_connection_details_button_displayed, 'Show Connection Details button displayed.'

        click(show_connection_details_button_pattern)

        more_information_button_displayed = exists(more_information_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert more_information_button_displayed, 'More information button displayed.'

        click(more_information_button_pattern)

        tls_connection_encrypted_message_displayed = exists(tls_connection_encrypted_message_pattern,
                                                            FirefoxSettings.FIREFOX_TIMEOUT)
        assert tls_connection_encrypted_message_displayed, 'The Technical Details section states that the connection' \
                                                           ' is encrypted via TLS 1.2, e.g. Connection Encrypted ' \
                                                           '(TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, 256 bit ' \
                                                           'keys, TLS 1.2).'
