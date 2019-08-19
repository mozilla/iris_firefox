# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='The form inputs that were previously saved in a normal session are remembered in Private '
                    'Browsing session.',
        locale=['en-US'],
        test_case_id='101666',
        test_suite_id='1826',
        preferences={'extensions.formautofill.available': 'on'},
    )
    def run(self, firefox):
        name_field_pattern = Pattern('name_field.png').similar(.6)
        private_browsing_image_pattern = PrivateWindow.private_window_pattern
        saved_profiles_pattern = Pattern('saved_profiles.png').similar(.6)
        if OSHelper.is_mac():
            additional_saved_profiles_pattern = Pattern('additional_saved_profiles.png').similar(.6)

        change_preference('browser.search.region', 'US')

        firefox.restart()

        navigate('https://luke-chang.github.io/autofill-demo/basic.html')

        input_data = ['Maria V. Griggs', 'Loblaws', '1223 Rainbow Drive', 'Youngstown, OH', '1223 Rainbow Drive',
                      '44512', 'US', '9079782387', 'maria_griggs@gmail.com']
        input_data_2 = ['Second V. Griggs', 'Loblaws_2', '1223 Rainbow Drive_2', 'Youngstown, OH_2',
                        '1223 Rainbow Drive_2', '44512', 'US', '9079782387', 'second_griggs@gmail.com']

        name_field_exists = exists(name_field_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert name_field_exists, 'The basic forms Autofill demo is opened'

        click(name_field_pattern)

        for fields in range(9):
            type(input_data[fields])
            type('\t')

        type('\n')

        restore_firefox_focus()

        time.sleep(FirefoxSettings.FIREFOX_TIMEOUT)

        click(name_field_pattern)

        for fields in range(9):
            type(input_data_2[fields])
            type('\t', interval=1)

        type('\n')

        time.sleep(FirefoxSettings.SHORT_FIREFOX_TIMEOUT)

        name_field = exists(name_field_pattern, FirefoxSettings.FIREFOX_TIMEOUT, Screen.TOP_THIRD)
        assert name_field, "name_field_pattern"

        click(name_field_pattern)

        double_click(name_field_pattern)

        if OSHelper.is_mac():
            saved_profiles_exists = exists(saved_profiles_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            additional_saved_profiles_exists = exists(additional_saved_profiles_pattern,
                                                      FirefoxSettings.FIREFOX_TIMEOUT)
            assert saved_profiles_exists or additional_saved_profiles_exists, 'The Name from the saved profile is ' \
                                                                              'displayed in the drop down'
        else:
            saved_profiles_exists = exists(saved_profiles_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            assert saved_profiles_exists, 'The Name from the saved profile is displayed in the drop down'

        new_private_window()

        private_browsing_opened = exists(private_browsing_image_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert private_browsing_opened, 'Private browsing window is opened'

        navigate('https://luke-chang.github.io/autofill-demo/basic.html')

        name_field_exists_private = exists(name_field_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert name_field_exists_private, 'The basic forms Autofill demo is opened'

        click(name_field_pattern)

        double_click(name_field_pattern)

        if OSHelper.is_mac():
            additional_saved_profiles_exists_private = exists(additional_saved_profiles_pattern.similar(0.6),
                                                              FirefoxSettings.TINY_FIREFOX_TIMEOUT)
            saved_profiles_exists_private = exists(saved_profiles_pattern, FirefoxSettings.TINY_FIREFOX_TIMEOUT)
            assert saved_profiles_exists_private or additional_saved_profiles_exists_private, 'The Name from the ' \
                'saved profile is displayed in the drop down in Private browsing'
        else:
            saved_profiles_exists_private = exists(saved_profiles_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            assert saved_profiles_exists_private, 'The Name from the saved profile is displayed in the drop down ' \
                                                  'in Private browsing'

        close_window()
