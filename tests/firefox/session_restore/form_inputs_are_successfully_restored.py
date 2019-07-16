# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Form inputs are successfully restored',
        test_case_id='114830',
        test_suite_id='68',
        locales=Locales.ENGLISH
    )
    def run(self, firefox):
        title_field_pattern = Pattern('title_field.png').similar(.6)

        input_data = ['Maria V. Griggs', 'Loblaws', '1223 Rainbow Drive']

        navigate('https://www.roboform.com/filling-test-all-fields')

        test_site_loaded = exists(title_field_pattern, Settings.SITE_LOAD_TIMEOUT, region=Screen.LEFT_HALF)
        assert test_site_loaded, 'The test website is successfully displayed.'

        title_field_width, title_field_height = title_field_pattern.get_size()

        in_field_focus = find(title_field_pattern).right(title_field_width * 3)

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

        assert entered_data == input_data, 'The data is displayed successfully.'

        if OSPlatform.MAC:
            quit_firefox()
        elif OSPlatform.MAC:
            click_hamburger_menu_option('Quit')
        else:
            click_hamburger_menu_option('Exit')

        firefox.restart()

        firefox_restarted = exists(LocalWeb.IRIS_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert firefox_restarted, 'Firefox restarted successfully'

        click_hamburger_menu_option('Restore')

        next_tab()

        test_site_loaded = exists(title_field_pattern, Settings.SITE_LOAD_TIMEOUT, region=Screen.LEFT_HALF)
        assert test_site_loaded, 'The test website is successfully displayed.'

        click(in_field_focus)

        restored_data = []

        for fields in range(3):
            edit_select_all()
            field_data = copy_to_clipboard()
            restored_data.append(str(field_data))
            type(Key.TAB)

        assert restored_data == input_data, 'The previous session is restored. The previously ' \
                                            'entered data is restored inside the form fields.'
