# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Credit Card form inputs that were previously saved in a normal session are remembered in Private '\
                    'Browsing session ',
        locale=['en-US'],
        test_case_id='101667',
        test_suite_id='1826',
        preferences={'extensions.formautofill.available': 'on',
                     'extensions.formautofill.creditCards.available': True}
    )
    def run(self, firefox):
        private_browsing_image_pattern = PrivateWindow.private_window_pattern
        find_in_preferences_field_pattern = AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED
        suggested_card_number_from_dropdown_pattern = Pattern('suggested_cc_number_from_dropdown.png')
        popup_name_on_card_field_pattern = Pattern('popup_name_on_card_field.png').similar(.6)
        expiration_month_dropdown_item_pattern = Pattern('expiration_month_dd_item.png')
        billing_address_dropdown_item_pattern = Pattern('billing_address_dd_item.png')
        expiration_year_dropdown_item_pattern = Pattern('expiration_year_dd_item.png')
        expiration_month_dropdown_pattern = Pattern('expiration_month_dropdown.png')
        saved_credit_cards_button_pattern = Pattern('saved_credit_cards_button.png')
        billing_address_dropdown_pattern = Pattern('billing_address_dropdown.png')
        address_first_name_field_pattern = Pattern('address_first_name_field.png')
        expiration_year_dropdown_pattern = Pattern('expiration_year_dropdown.png')
        popup_card_number_field_pattern = Pattern('popup_card_number_field.png')
        saved_addresses_button_pattern = Pattern('saved_addresses_button.png')
        card_type_dropdown_item_pattern = Pattern('card_type_dd_item.png')
        card_type_dropdown_pattern = Pattern('card_type_dropdown.png')
        card_number_field_pattern = Pattern('card_number_field.png')
        visa_logo_pattern = Pattern('visa_logo.png').similar(0.7)
        submit_button_pattern = Pattern('submit_button.png')
        save_button_pattern = Pattern('save_button.png')
        add_button_pattern = Pattern('add_button.png')

        change_preference('browser.search.region', 'US')

        firefox.restart(LocalWeb.FIREFOX_TEST_SITE, image=LocalWeb.FIREFOX_LOGO)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        navigate('about:preferences#privacy')

        search_field_exists = exists(find_in_preferences_field_pattern, FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        assert search_field_exists, 'Preferences page is opened'

        paste('Autofill')

        saved_addresses_button_exists = exists(saved_addresses_button_pattern, FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        assert saved_addresses_button_exists, '\'Saved addresses\' button is displayed on the Preferences page'

        click(saved_addresses_button_pattern)

        add_button_exists = exists(add_button_pattern, FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        assert add_button_exists, '\'Add\' button is displayed on the \'Saved addresses\' popup'

        click(add_button_pattern)

        address_first_name_field_exists = exists(address_first_name_field_pattern, FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        assert address_first_name_field_exists, '\'First Name\' field is displayed on the \'Add new address\' popup'

        click(address_first_name_field_pattern)

        paste('Maria')

        save_button_exists = exists(save_button_pattern, FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        assert save_button_exists, '\'Save\' button is displayed on the \'Add new address\' popup'

        click(save_button_pattern)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        type(Key.ESC)

        try:
            add_button_disappeared = wait_vanish(add_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            assert add_button_disappeared, 'Address list popup dissapeared.'
        except FindError:
            raise FindError('Entered data did not vanish after clicking the \'Submit button\'')

        saved_credit_cards_button_exists = exists(saved_credit_cards_button_pattern, FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        assert saved_credit_cards_button_exists, '\'Saved credit cards\' button is displayed on the Preferences page'

        click(saved_credit_cards_button_pattern)

        add_button_exists = exists(add_button_pattern, FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        assert add_button_exists, '\'Add\' button is displayed on the \'Saved credit cards\' popup'

        click(add_button_pattern)

        card_type_dropdown_exists = exists(card_type_dropdown_pattern.similar(0.6), FirefoxSettings.FIREFOX_TIMEOUT)
        assert card_type_dropdown_exists, '\'Card type\' dropdown is displayed on the \'Edit Credit Card\' popup'

        click(card_type_dropdown_pattern.similar(0.6))

        card_type_dropdown_item_exists = exists(card_type_dropdown_item_pattern, FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        assert card_type_dropdown_item_exists, '\'Visa\' option is available on the \'Card type\' dropdown'

        click(card_type_dropdown_item_pattern)

        popup_card_number_field_exists = exists(popup_card_number_field_pattern, FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        assert popup_card_number_field_exists, '\'Card Number\' field is displayed on the \'Edit Credit Card\' popup'

        click(popup_card_number_field_pattern)

        paste('4443695376356261')

        popup_name_on_card_field_exists = exists(popup_name_on_card_field_pattern, FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        assert popup_name_on_card_field_exists, '\'Name on card\' field is displayed on the \'Edit Credit Card\' popup'

        click(popup_name_on_card_field_pattern)

        paste('Maria')

        expiration_month_dropdown_exists = exists(expiration_month_dropdown_pattern, FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        assert expiration_month_dropdown_exists, '\'Expiration month\' dropdown is displayed on the ' \
                                                 '\'Edit Credit Card\' popup'

        click(expiration_month_dropdown_pattern)

        expiration_month_dropdown_item_exists = exists(expiration_month_dropdown_item_pattern,
                                                       FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        assert expiration_month_dropdown_item_exists, '\'05 - May\' option is displayed on the dropdown ' \
                                                      '\'Expiration month\''

        click(expiration_month_dropdown_item_pattern)

        expiration_year_dropdown_exists = exists(expiration_year_dropdown_pattern, FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        assert expiration_year_dropdown_exists, '\'Expiration year\' dropdown is displayed on the ' \
                                                '\'Edit Credit Card\' popup'

        click(expiration_year_dropdown_pattern)

        expiration_year_dropdown_item_exists = exists(expiration_year_dropdown_item_pattern,
                                                      FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        assert expiration_year_dropdown_item_exists, '\'2029\' option is available on the \'Expiration year\' dropdown'

        click(expiration_year_dropdown_item_pattern)

        billing_address_dropdown_exists = exists(billing_address_dropdown_pattern, FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        assert billing_address_dropdown_exists, '\'Billing address\' dropdown is displayed on the ' \
                                                '\'Edit Credit Card\' popup'

        click(billing_address_dropdown_pattern)

        billing_address_dropdown_item_exists = exists(billing_address_dropdown_item_pattern,
                                                      FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        assert billing_address_dropdown_item_exists, 'Previously saved address displayed on the \'Billing address\' ' \
                                                     'dropdown'

        click(billing_address_dropdown_item_pattern)

        save_button_exists = exists(save_button_pattern, FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        assert save_button_exists, '\'Save\' button is displayed on the \'Edit Credit Card\' popup'

        click(save_button_pattern)

        credit_card_successfully_saved = exists(visa_logo_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert credit_card_successfully_saved, 'Credit card was successfully saved'

        navigate('https://luke-chang.github.io/autofill-demo/basic_cc.html')

        page_opened = exists(submit_button_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert page_opened, 'Test page is opened.'

        card_number_field_exists = exists(card_number_field_pattern, FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        assert card_number_field_exists, '\'Card number\' field is displayed on the page'

        click(card_number_field_pattern)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT+1)

        click(card_number_field_pattern)

        saved_credit_card_number_exists = exists(suggested_card_number_from_dropdown_pattern.similar(0.6),
                                                 FirefoxSettings.FIREFOX_TIMEOUT) 
        assert saved_credit_card_number_exists, 'The Credit Card number from the saved profile is displayed in the ' \
                                                'dropdown'

        new_private_window()
        navigate('https://luke-chang.github.io/autofill-demo/basic_cc.html')

        private_window_opened = exists(private_browsing_image_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert private_window_opened, 'New private window is opened'

        page_opened_in_private_window = exists(submit_button_pattern,  FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert page_opened_in_private_window, 'Test page is opened in a new Private window'

        card_number_field_exists = exists(card_number_field_pattern, FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        assert card_number_field_exists, '\'Card Number\' field is displayed on the page'

        click(card_number_field_pattern)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT+1)

        click(card_number_field_pattern)

        saved_credit_card_number_exists = exists(suggested_card_number_from_dropdown_pattern,
                                                 FirefoxSettings.FIREFOX_TIMEOUT)

        assert saved_credit_card_number_exists, 'Saved CC profile is displayed in the suggestions panel.'

        close_window()
