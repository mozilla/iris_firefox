# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Form inputs are not saved if they are performed inside a private browsing session.'
        self.test_case_id = '101669'
        self.test_suite_id = '1956'
        self.locales = ['en-US']
        self.set_profile_pref({'extensions.formautofill.available': 'on'})

    def run(self):
        private_browsing_image_pattern = PrivateWindow.private_window_pattern
        submit_button_pattern = Pattern('submit_button.png').similar(.6)
        save_button_pattern = Pattern('save_button.png')
        name_field_pattern = Pattern('name_field.png').similar(.6)
        organization_field_pattern = Pattern('organization_field.png').similar(.6)
        address_field_pattern = Pattern('street_address_field.png').similar(.6)
        address_level_2_pattern = Pattern('address_level_2_field.png').similar(.6)
        address_level_1_pattern = Pattern('address_level_1_field.png').similar(.6)
        postal_code_pattern = Pattern('postal_code_field.png').similar(.6)
        country_code_field_pattern = Pattern('country_code_field.png').similar(.6)
        telephone_field_pattern = Pattern('telephone_field.png').similar(.6)
        email_field_pattern = Pattern('email_field.png').similar(.6)
        find_in_prefs_field_pattern = Pattern('find_in_prefs_field.png').similar(.6)
        saved_addresses_button_pattern = Pattern('saved_addresses_button.png').similar(.6)
        name_in_saved_addresses_pattern = Pattern('name_in_saved_addresses.png')

        new_private_window()
        navigate('https://luke-chang.github.io/autofill-demo/basic.html')
        page_opened_in_private_browsing_mode = exists(private_browsing_image_pattern) \
                                               and exists(submit_button_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, page_opened_in_private_browsing_mode, 'Test page is opened in a new private window.')

        input_data = {
            name_field_pattern: ['Maria V. Griggs', 'Name'],
            organization_field_pattern: ['Loblaws', 'Organization'],
            address_field_pattern: ['1223 Rainbow Drive', 'Address'],
            address_level_2_pattern: ['Youngstown, OH', 'Address level 2'],
            address_level_1_pattern: ['1223 Rainbow Drive', 'Address level 1'],
            postal_code_pattern: ['44512', 'Postal code'],
            country_code_field_pattern: ['US', 'Country code'],
            telephone_field_pattern: ['9079782386', 'Telephone'],
            email_field_pattern: ['maria_griggs@gmail.com', 'Email']
        }

        for field in input_data:
            field_exists = exists(field)
            assert_true(self, field_exists, '{} field exists'.format(input_data[field][1]))
            click(field)
            type(input_data[field][0])

        click(submit_button_pattern)

        tooltip_displayed = exists(save_button_pattern)
        assert_false(self, tooltip_displayed, 'The form gets successfully submitted but no "tooltip" to save the input '
                                              'is displayed.')

        close_window()

        private_browsing_image_exists = exists(private_browsing_image_pattern)
        assert_false(self, private_browsing_image_exists, 'Normal browsing session is displayed')

        navigate('about:preferences#privacy')
        find_in_prefs_field_exists = exists(find_in_prefs_field_pattern)
        assert_true(self, find_in_prefs_field_exists, 'Preferences search field is available')
        click(find_in_prefs_field_pattern)

        type('Autofill')
        saved_addresses_button_exists = exists(saved_addresses_button_pattern)
        assert_true(self, saved_addresses_button_exists, '"Saved addresses" button is available')
        click(saved_addresses_button_pattern)

        saved_address_exists = exists(name_in_saved_addresses_pattern)
        assert_false(self, saved_address_exists, 'The submitted information in the private session '
                                                 'is not displayed in the saved Addresses panel')
        close_window()
