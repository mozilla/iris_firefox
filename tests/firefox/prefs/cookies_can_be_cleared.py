# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Firefox can be set to no longer accept third-party cookies.',
        locale=['en-US'],
        test_case_id='106156',
        test_suite_id='1826',
        blocked_by={'id': '1568911', 'platform': OSPlatform.ALL}
    )
    def run(self, firefox):
        clear_data_button_pattern = Pattern('clear_button.png')
        confirm_clear_data_pattern = Pattern('confirm_clear_data.png')
        open_clear_data_window_pattern = Pattern('open_clear_data_window.png')
        zero_bytes_cache_pattern = Pattern('zero_bytes_cache.png')
        cached_web_content_item_pattern = Pattern('cached_web_content_item.png').similar(.6)
        cookies_and_site_data_item_pattern = Pattern('cookies_and_site_data_item.png').similar(.6)

        navigate('about:preferences#privacy')

        preferences_opened = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED)
        assert preferences_opened, 'Preferences page is opened'

        open_find()

        paste('clear data')

        clear_data_button_selected = exists(open_clear_data_window_pattern)
        assert clear_data_button_selected, '"Clear data" button is selected'

        click(open_clear_data_window_pattern)

        clear_data_window_opened = exists(clear_data_button_pattern.similar(0.9))
        assert clear_data_window_opened, 'The "Clear Data" subdialog is displayed'

        cached_web_content_item_displayed = exists(cached_web_content_item_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert cached_web_content_item_displayed, 'Cached Web Content item displayed'

        click(cached_web_content_item_pattern)

        cached_web_content_item_unselected = find_in_region_from_pattern(cached_web_content_item_pattern,
                                                                         AboutPreferences.UNCHECKED_BOX)
        assert cached_web_content_item_unselected, 'Cached Web Content item can be unselected'

        click(cached_web_content_item_pattern)

        cached_web_content_item_selected = find_in_region_from_pattern(cached_web_content_item_pattern,
                                                                       AboutPreferences.CHECKED_BOX)
        assert cached_web_content_item_selected, 'Cached Web Content item can be selected'

        cookies_and_site_data_displayed = exists(cookies_and_site_data_item_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert cookies_and_site_data_displayed, 'Cookies and Site Data item displayed'

        click(cookies_and_site_data_item_pattern)

        cookies_and_site_data_unselected = find_in_region_from_pattern(cookies_and_site_data_item_pattern,
                                                                       AboutPreferences.UNCHECKED_BOX)
        assert cookies_and_site_data_unselected, 'Cookies and Site Data item can be unselected'

        click(cookies_and_site_data_item_pattern)

        cookies_and_site_data_selected = find_in_region_from_pattern(cookies_and_site_data_item_pattern,
                                                                     AboutPreferences.CHECKED_BOX)
        assert cookies_and_site_data_selected, 'Cookies and Site Data item can be selected'

        edit_select_all()

        edit_copy()

        warning_text_displayed = get_clipboard().replace('\n', '').replace('\r', '')
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
        assert 'Clearing all cookies and site data stored by Firefox may sign you out of websites and remove offline ' \
               'web content. Clearing cache data will not affect your logins.' in warning_text_displayed, \
            '"Clearing all cookies and site data stored by Firefox may sign you out of websites and remove offline ' \
            'web content. Clearing cache data will not affect your logins." - warning test displayed'

        click(clear_data_button_pattern)

        clear_message_appeared = exists(confirm_clear_data_pattern)
        assert clear_message_appeared, 'The "Clear all cookies and site data" pop-up is displayed'

        edit_select_all()

        edit_copy()

        warning_text_displayed = get_clipboard().replace('\n', '').replace('\r', '')
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT / 2)
        assert 'Selecting ‘Clear Now’ will clear all cookies and site data stored by Firefox. This may sign you out ' \
               'of websites and remove offline web content.' in warning_text_displayed, \
            '"Selecting ‘Clear Now’ will clear all cookies and site data stored by Firefox. This may sign you out of ' \
            'websites and remove offline web content." - warning test displayed'

        click(confirm_clear_data_pattern)

        data_cleared = exists(zero_bytes_cache_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert data_cleared, 'The pop-up and the subdialog are dismissed and the amount of disk space used is ' \
                             'changed back to 0 MB'
