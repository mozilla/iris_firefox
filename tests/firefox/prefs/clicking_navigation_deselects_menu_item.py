# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bug 1524210 - Clicking near the about:preferences navigation menu deselects the previously '
                    'selected menu item',
        test_case_id='249027',
        test_suite_id='2241',
        locale=['en-US'],
    )
    def run(self, firefox):
        navigate('about:preferences')

        page_loaded = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_NOT_SELECTED,
                             FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert page_loaded, 'about:preferences page loaded'

        click(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_NOT_SELECTED)

        privacy_selected = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED,
                                  FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        screen_center_location = Location(Screen.SCREEN_WIDTH//2, Screen.SCREEN_HEIGHT//2)
        hover(screen_center_location)

        always_radio_not_selected_pattern = AboutPreferences.Privacy.CONTENT_TRACKING_TRACKERS_ALWAYS_RADIO_NOT_SELECTED
        page_displayed = scroll_until_pattern_found(always_radio_not_selected_pattern, scroll, (-20,), 100,
                                                    FirefoxSettings.TINY_FIREFOX_TIMEOUT // 3)

        assert privacy_selected and page_displayed, 'The button is selected and the corresponding page is displayed.'

        empty_space_near_navigation_menu_location = find(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED)

        home_width = NavBar.HOME_BUTTON.get_size()[0]

        empty_space_near_privacy_button_location = Location(
            empty_space_near_navigation_menu_location.x - (home_width * 1.5),
            empty_space_near_navigation_menu_location.y)

        click(empty_space_near_privacy_button_location)

        button_remains_selected = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED.similar(0.95),
                                         FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert button_remains_selected, 'The selected button from step 3 remains selected and has a blue color. ' \
                                        'NOTE: In the builds affected by this bug the button gets deselected. ' \
                                        'To see behaviour, click here.' \
                                        '[https://bug1524210.bmoattachments.org/attachment.cgi?id=9040357]'
