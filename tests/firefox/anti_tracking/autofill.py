# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *
from targets.firefox.firefox_ui.private_window import PrivateWindow
from src.configuration.config_parser import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Autofill is not automatically performed in Private Browsing.',
        test_case_id='101673',
        test_suite_id='1826',
        locale=['en-US'],
        enabled=False
    )
    def run(self, firefox):
        private_browsing_image_pattern = PrivateWindow.private_window_pattern
        twitter_tab_favicon_pattern = Pattern('twitter_favicon.png')
        login_field_pattern = Pattern('login_field.png')
        password_field_pattern = Pattern('password_field.png')
        save_credentials_button_pattern = Pattern('save_button.png')
        autofill_asterisks_pattern = Pattern('autofill_asterisks.png')

        twitter_login = get_config_property('Twitter', 'username')
        twitter_password = get_config_property('Twitter', 'password')

        navigate('twitter.com')
        twitter_tab_favicon_exists = exists(twitter_tab_favicon_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert twitter_tab_favicon_exists, 'Twitter page successfully opens'

        login_field_exists = exists(login_field_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert login_field_exists, 'Login field is displayed on the page'
        
        click(login_field_pattern)
        
        type(twitter_login)

        password_field_exists = exists(password_field_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert password_field_exists, 'Password field is displayed on the page'
        
        click(password_field_pattern)
        
        type(twitter_password)
        type(Key.ENTER)

        save_button_exists = exists(save_credentials_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert save_button_exists, 'Save button displays after entering twitter login and password'

        click(save_credentials_button_pattern)

        new_private_window()

        new_private_window_exists = exists(private_browsing_image_pattern)
        assert new_private_window_exists, 'The private browsing tab is displayed.'

        navigate('twitter.com')

        twitter_tab_favicon_exists = exists(twitter_tab_favicon_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert twitter_tab_favicon_exists, 'Twitter page successfully opens'

        save_credentials_exist = exists(autofill_asterisks_pattern)
        assert save_credentials_exist is not True, 'The log in information is not autofilled.'

        close_window()
