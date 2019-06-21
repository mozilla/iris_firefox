# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Credit Card form inputs are not saved if they are given inside a Private Browsing session.',
        locale=['en-US'],
        test_case_id='101668',
        test_suite_id='1826',
        preferences={'extensions.formautofill.available': 'on',
                     'extensions.formautofill.creditCards.available': True}
    )
    def run(self, firefox):
        private_browsing_image_pattern = PrivateWindow.private_window_pattern
        visa_logo_pattern = Pattern('visa_logo.png')
        card_number_field_pattern = Pattern('card_number_field.png').similar(.6)
        expiration_month_field_pattern = Pattern('expiration_month_field.png').similar(.6)
        expiration_year_field_pattern = Pattern('expiration_year_field.png').similar(.6)
        csc_field_pattern = Pattern('csc_field.png').similar(.6)
        submit_button_pattern = Pattern('submit_button.png').similar(.6)
        entered_csc_pattern = Pattern('entered_csc.png').similar(.6)
        find_in_preferences_field_pattern = Pattern('find_in_preferences_field.png').similar(.6)
        saved_credit_cards_button_pattern = Pattern('saved_credit_cards_button.png').similar(.6)
        name_field_pattern = Pattern('name_field.png').similar(.6)

        change_preference('browser.search.region', 'US')

        new_private_window()

        navigate('https://luke-chang.github.io/autofill-demo/basic_cc.html')
        page_opened_in_private_browsing_mode = exists(
            private_browsing_image_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT) and exists(
            submit_button_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert page_opened_in_private_browsing_mode, 'Test page is opened in a new private window.'

        input_data = {
            name_field_pattern: ['Maria', 'Name'],
            card_number_field_pattern: ['4929094911200312', 'Card Number'],
            expiration_month_field_pattern: ['9', 'Expiration month'],
            expiration_year_field_pattern: ['2020', 'Expiration year'],
            csc_field_pattern: ['903', 'CSC']
        }

        for field in input_data:
            field_exists = exists(field)
            assert field_exists, '{} field exists'.format(input_data[field][1])

            click(field)

            type(input_data[field][0])

        click(submit_button_pattern)

        left_half_region = Region(0, 0, Screen.SCREEN_WIDTH//2, Screen.SCREEN_HEIGHT)
        try:
            entered_csc_on_page = wait_vanish(entered_csc_pattern, region=left_half_region)
            assert entered_csc_on_page, 'Credit Card Information is successfully entered and submitted.'
        except FindError:
            raise FindError('Entered data did not vanish after clicking the \'Submit button\'')

        close_window()

        private_browsing_image_exists = exists(private_browsing_image_pattern)
        assert private_browsing_image_exists is not True, 'Normal browsing session is displayed'

        navigate('about:preferences#privacy')

        find_in_preferences_field_exists = exists(find_in_preferences_field_pattern)
        assert find_in_preferences_field_exists, 'Preferences search field is available'

        click(find_in_preferences_field_pattern)

        type('Autofill')

        saved_credit_cards_button_exists = exists(saved_credit_cards_button_pattern)
        assert saved_credit_cards_button_exists, '\'Saved credit cards\' button is displayed on the page'

        click(saved_credit_cards_button_pattern)

        visa_logo_exists = exists(visa_logo_pattern)
        assert visa_logo_exists is not True, 'The submitted credentials in the private session are not displayed ' \
                                             'inside the Saved CCs panel.'
