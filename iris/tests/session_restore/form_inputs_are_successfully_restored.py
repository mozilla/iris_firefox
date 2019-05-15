# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Form inputs are successfully restored'
        self.test_case_id = '114830'
        self.test_suite_id = '68'
        self.locales = ['en-US']

    def run(self):
        title_field_pattern = Pattern('title_field.png')

        input_data = ['Maria V. Griggs', 'Loblaws', '1223 Rainbow Drive']

        navigate('https://www.roboform.com/filling-test-all-fields')

        test_site_loaded = exists(title_field_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, test_site_loaded, 'The test website is successfully displayed.')

        title_field_width, title_field_height = title_field_pattern.get_size()

        in_field_focus = find(title_field_pattern).right(title_field_width*3)

        click(in_field_focus)

        for fields in range(3):
            type(input_data[fields])
            type(Key.TAB)

        click(in_field_focus)

        entered_data = []

        for fields in range(3):
            edit_select_all()
            field_data = copy_to_clipboard()
            entered_data.append(str(field_data))
            type(Key.TAB)

        assert_true(self, entered_data == input_data, 'The data is displayed successfully.')

        if Settings.is_mac():
            quit_firefox()
        elif Settings.is_linux():
            click_hamburger_menu_option('Quit')
        else:
            click_hamburger_menu_option('Exit')

        status = self.firefox_runner.process_handler.wait(Settings.FIREFOX_TIMEOUT)
        if status is None:
            self.firefox_runner.stop()
            self.firefox_runner = None

        self.firefox_runner = launch_firefox(self.browser.path, self.profile_path, self.base_local_web_url)
        self.firefox_runner.start()

        firefox_restarted = exists(LocalWeb.IRIS_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, firefox_restarted, 'Firefox restarted successfully')

        click_hamburger_menu_option('Restore')

        next_tab()

        click(in_field_focus)

        restored_data = []

        for fields in range(3):
            edit_select_all()
            field_data = copy_to_clipboard()
            restored_data.append(str(field_data))
            type(Key.TAB)

        assert_true(self, restored_data == input_data, 'The previous session is restored. The previously entered data '
                                                       'is restored inside the form fields.')
