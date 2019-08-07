# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Autoscrolling can be successfully enabled/disabled',
        test_case_id='143581',
        test_suite_id='2241',
        locale=['en-US'],
    )
    def run(self, firefox):

        about_preferences_general_url_pattern = Pattern('about_preferences_general_url.png')
        preferences_general_option_pattern = Pattern('preferences_general_option.png')
        use_autoscrolling_checked_pattern = Pattern('use_autoscrolling_checked.png')
        use_autoscrolling_unchecked_pattern = Pattern('use_autoscrolling_unchecked.png')
        autoscrolling_enabled_pattern = Pattern('autoscrolling_enabled.png')

        location = Location(Screen.SCREEN_WIDTH / 1.5, Screen.SCREEN_HEIGHT / 2)

        navigate('about:preferences#general')

        about_preferences_general_url_exists = exists(about_preferences_general_url_pattern,
                                                      FirefoxSettings.FIREFOX_TIMEOUT)
        assert about_preferences_general_url_exists, 'The about:preferences page is successfully loaded'

        preferences_general_option_exists = exists(preferences_general_option_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert preferences_general_option_exists, 'The options for "General" section are displayed'

        move(location)

        if OSHelper.is_linux():
            use_autoscrolling_unchecked_exists = scroll_until_pattern_found(use_autoscrolling_unchecked_pattern,
                                                                            Mouse().scroll, (0, -Screen.SCREEN_HEIGHT),
                                                                            20, FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
            assert use_autoscrolling_unchecked_exists, 'The option is not checked by default'

            click(use_autoscrolling_unchecked_pattern)

            use_autoscrolling_checked_exists = exists(use_autoscrolling_checked_pattern,
                                                      FirefoxSettings.FIREFOX_TIMEOUT)
            assert use_autoscrolling_checked_exists, 'The option is checked'

        else:
            use_autoscrolling_checked_exists = scroll_until_pattern_found(use_autoscrolling_checked_pattern,
                                                                          Mouse().scroll, (0, -Screen.SCREEN_HEIGHT),
                                                                          20, FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
            assert use_autoscrolling_checked_exists, 'The option is checked by default'

        middle_click(location)

        autoscrolling_enabled_exists = exists(autoscrolling_enabled_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert autoscrolling_enabled_exists, 'Autoscrolling is enabled'

        click(location)

        click(use_autoscrolling_checked_pattern)

        use_autoscrolling_unchecked_exists = exists(use_autoscrolling_unchecked_pattern,
                                                    FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert use_autoscrolling_unchecked_exists, 'The option is successfully unchecked'

        middle_click(location)

        autoscrolling_enabled_exists = exists(autoscrolling_enabled_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert autoscrolling_enabled_exists is False, 'The autoscrolling is disabled'
