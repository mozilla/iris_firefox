# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Private Browsing window is not restored after Firefox crash'
        self.test_case_id = '101666'
        self.test_suite_id = '1956'
        self.locales = ['en-US']

    def run(self):
        name_field_pattern = Pattern('name_field.png').similar(.6)
        private_browsing_image_pattern = PrivateWindow.private_window_pattern
        saved_profiles_pattern = Pattern('saved_profiles.png').similar(.6)

        navigate('https://luke-chang.github.io/autofill-demo/basic.html')

        input_data = ['Maria V. Griggs', 'Loblaws', '1223 Rainbow Drive', 'Youngstown, OH', '1223 Rainbow Drive',
                      '44512', 'US', '9079782387', 'maria_griggs@gmail.com']
        input_data_2 = ['Second V. Griggs', 'Loblaws_2', '1223 Rainbow Drive_2', 'Youngstown, OH_2',
                        '1223 Rainbow Drive_2', '44512', 'US', '9079782387', 'second_griggs@gmail.com']

        name_field_exists = exists(name_field_pattern)
        assert_true(self, name_field_exists, 'The basic forms Autofill demo is opened')

        click(name_field_pattern)

        for fields in range(9):
            type(input_data[fields])
            type('\t')

        type('\n')

        restore_firefox_focus()
        click(name_field_pattern)

        for fields in range(9):
            type(input_data_2[fields])
            type('\t')

        type('\n')

        click(name_field_pattern)
        double_click(name_field_pattern)

        saved_profiles_exists = exists(saved_profiles_pattern)
        assert_true(self, saved_profiles_exists, 'The Name from the saved profile is displayed in the drop down')

        new_private_window()

        private_browsing_opened = exists(private_browsing_image_pattern)
        assert_true(self, private_browsing_opened, 'Private browsing window is opened')

        navigate('https://luke-chang.github.io/autofill-demo/basic.html')

        name_field_exists_private = exists(name_field_pattern)
        assert_true(self, name_field_exists_private, 'The basic forms Autofill demo is opened')

        click(name_field_pattern)
        double_click(name_field_pattern)

        saved_profiles_exists_private = exists(saved_profiles_pattern)
        assert_true(self, saved_profiles_exists_private, 'The Name from the saved profile is displayed in the drop down'
                                                         'in Private browsing')

        close_window()
