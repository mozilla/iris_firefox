# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description=' Websites using an Extended Validation certificate with their domain are properly loaded '
                    'and depicted in the Location Bar ',
        test_case_id='3952',
        test_suite_id='69',
        locale=['en-US'],
    )
    def run(self, firefox):
        bad_ssl_green_logo_pattern = Pattern('bad_ssl_green_logo.png')
        show_connection_details_button_pattern = Pattern('show_connection_details_button.png')
        more_information_button_pattern = Pattern('more_information_button.png')

        navigate('https://extended-validation.badssl.com/')

        bad_ssl_page_loaded = exists(bad_ssl_green_logo_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert bad_ssl_page_loaded, 'Bad SSL page sucessfully loaded'

        connection_is_secure = exists(LocationBar.SECURE_CONNECTION_LOCK, FirefoxSettings.FIREFOX_TIMEOUT)
        assert connection_is_secure, 'The connection is secure.'

        connection_lock_location = find(LocationBar.SECURE_CONNECTION_LOCK)
        connection_lock_width, connection_lock_height = LocationBar.SECURE_CONNECTION_LOCK.get_size()
        connection_lock_region = Region(connection_lock_location.x, connection_lock_location.y,
                                        connection_lock_width * 20, connection_lock_height)

        domain_owner_displayed = exists('Mozilla Foundation (US)', FirefoxSettings.FIREFOX_TIMEOUT,
                                        connection_lock_region)
        assert domain_owner_displayed, 'The owner of the domain is highlighted in green, next to the URL, e.g. ' \
                                       'Mozilla Foundation (US).'

        edit_select_all()

        edit_copy()

        text_displayed = get_clipboard().replace('\n', '').replace('\r', '')
        assert 'extended-validation.badssl.com' in text_displayed, 'The URL is properly loaded and green background ' \
                                                                   'page is displayed, containing a string saying: ' \
                                                                   'extended-validation.badssl.com'

        click(LocationBar.IDENTITY_ICON)

        domain_owner_displayed_after_click = exists('Mozilla Foundation (US)', FirefoxSettings.FIREFOX_TIMEOUT,
                                                    connection_lock_region)
        assert domain_owner_displayed_after_click, 'Mozilla Foundation is displayed when the user clicks the icon ' \
                                                   'next to the URL.'

        show_connection_details_button_displayed = exists(show_connection_details_button_pattern,
                                                          FirefoxSettings.FIREFOX_TIMEOUT)
        assert show_connection_details_button_displayed, 'Show Connection Details button displayed.'

        click(show_connection_details_button_pattern)

        certificate_additional_details_region = Region(connection_lock_location.x,
                                                       connection_lock_location.y + connection_lock_height,
                                                       connection_lock_width * 10, connection_lock_height * 20)

        certificate_additional_details_popup_displayed = exists(more_information_button_pattern,
                                                                FirefoxSettings.FIREFOX_TIMEOUT)
        assert certificate_additional_details_popup_displayed, 'Certificate additional details pop-up displayed.'

        certificate_additional_details = ['Mozilla Foundation', 'Mountain View', 'California, US']

        detail_find = 0
        certificate_additional_details_displayed = False

        for text in certificate_additional_details:
            details_displayed = exists(text, FirefoxSettings.SHORT_FIREFOX_TIMEOUT,
                                       certificate_additional_details_region)
            if details_displayed:
                detail_find += 1

        if detail_find == 3:
            certificate_additional_details_displayed = True

        assert certificate_additional_details_displayed, 'Additional details displayed regarding the certificate, ' \
                                                         'e.g. certificate issues, the physical address of the ' \
                                                         'certificate owner, etc.'
