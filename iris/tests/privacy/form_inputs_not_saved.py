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

    def run(self):
        private_browsing_image_pattern = PrivateWindow.private_window_pattern
        submit_button_pattern = Pattern('submit_button.png')
        input_field_pattern = Pattern('input_field.png')
        save_button_pattern = Pattern('save_button.png')
        input_text_pattern = Pattern('input_text.png')

        change_preference('extensions.formautofill.available', 'on')

        new_private_window()
        navigate('https://luke-chang.github.io/autofill-demo/basic.html')
        page_opened_in_private_browsing_mode = exists(private_browsing_image_pattern) and exists(submit_button_pattern)
        assert_true(self, page_opened_in_private_browsing_mode, 'Test page is opened in a new private window.')

        input_fields_available = exists(submit_button_pattern)
        assert_true(self, input_fields_available, 'Input fields available.')

        for field_count in range(9):
            click(input_field_pattern)
            type('valid input data')
            type(Key.TAB)

        data_entered_into_every_field = exists(input_text_pattern)
        assert_true(self, data_entered_into_every_field, 'Valid data successfully entered into every field.')

        click(submit_button_pattern)

        tooltip_displayed = exists(save_button_pattern)
        assert_false(self, tooltip_displayed, 'The form was successfully submitted but no tooltip was displayed.')

        close_window()
        private_browsing_image_exists = exists(private_browsing_image_pattern)
        assert_false(self, private_browsing_image_exists, 'Normal browsing session is displayed')

        close_window()
