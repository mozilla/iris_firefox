# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Private Browsing window is not restored after Firefox crash'
        self.test_case_id = '101748'
        self.test_suite_id = '1826'
        self.locales = ['en-US']

    def run(self):
        name_field_pattern = Pattern('name_field.png')
        submit_button_pattern = Pattern('submit_button.png')
        private_browsing_image_pattern = PrivateWindow.private_window_pattern
        organization_field_pattern = Pattern('organization_field.png')
        address_field_pattern = Pattern('street_address_field.png')
        address_level_2_pattern = Pattern('address_level_2_field.png')
        address_level_1_pattern = Pattern('address_level_1_field.png')
        postal_code_pattern = Pattern('postal_code_field.png')
        country_code_field_pattern = Pattern('country_code_field.png')
        telephone_field_pattern = Pattern('telephone_field.png')
        email_field_pattern = Pattern('email_field.png')
        saved_profiles_pattern = Pattern('saved_profiles.png')

        navigate('https://luke-chang.github.io/autofill-demo/basic.html')

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

        input_data = {
            name_field_pattern: ['Second S. Griggs', 'Name'],
            organization_field_pattern: ['Loblaws_2', 'Organization'],
            address_field_pattern: ['1223 Rainbow Drive_2', 'Address'],
            address_level_2_pattern: ['Youngstown, OH_2', 'Address level 2'],
            address_level_1_pattern: ['1223 Rainbow Drive_2', 'Address level 1'],
            postal_code_pattern: ['44512', 'Postal code'],
            country_code_field_pattern: ['US', 'Country code'],
            telephone_field_pattern: ['9079782387', 'Telephone'],
            email_field_pattern: ['second_griggs@gmail.com', 'Email']
        }

        for field in input_data:
            field_exists = exists(field)
            assert_true(self, field_exists, '{} field exists'.format(input_data[field][1]))

            click(field)
            type(input_data[field][0])

        click(submit_button_pattern)

        click(name_field_pattern)
        double_click(name_field_pattern)

        saved_profiles_exists = exists(saved_profiles_pattern)
        assert_true(self, saved_profiles_exists, 'The Name from the saved profile is displayed in the drop down')

        new_private_window()

        private_browsing_opened = exists(private_browsing_image_pattern)
        assert_true(self, private_browsing_opened, 'Private browsing window is opened')

        navigate('https://luke-chang.github.io/autofill-demo/basic.html')

        click(name_field_pattern)
        double_click(name_field_pattern)

        saved_profiles_exists_private = exists(saved_profiles_pattern)
        assert_true(self, saved_profiles_exists_private, 'The Name from the saved profile is displayed in the drop down'
                                                         'in Private browsing')

        close_window()
