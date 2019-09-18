# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='[First Time User] Close Firefox browser when updating safebrowsing DB',
        test_case_id='50360',
        test_suite_id='69',
        locale=['en-US'],

    )
    def run(self, firefox):
        url_classifier_title_pattern = Pattern('url_classifier_title.png')
        google4_row_pattern = Pattern('google4_row.png')
        trigger_update_button_pattern = Pattern('trigger_update_button.png')
        success_status_pattern = Pattern('success_status.png')
        local_directory_row_pattern = Pattern('local_directory_row.png').similar(.7)
        show_in_button_pattern = Pattern('show_in_button.png').similar(.7)
        profile_default_title_pattern = Pattern('profile_default_title.png')

        navigate('about:profiles')

        about_profiles_page_opened = exists(profile_default_title_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert about_profiles_page_opened, 'About profiles page opened'

        profile_default_title_location = find(profile_default_title_pattern)
        profile_default_title_width, profile_default_title_height = profile_default_title_pattern.get_size()
        profile_default_region = Region(profile_default_title_location.x, profile_default_title_location.y,
                                        profile_default_title_width, profile_default_title_height * 9)

        local_directory_row_location = find(local_directory_row_pattern, profile_default_region)
        local_directory_row_width, local_directory_row_height = local_directory_row_pattern.get_size()
        local_directory_row_region = Region(local_directory_row_location.x, local_directory_row_location.y,
                                            local_directory_row_width * 10, local_directory_row_height)

        show_in_button_found = exists(show_in_button_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT,
                                      local_directory_row_region)
        assert show_in_button_found, 'Show in finder/folder button found'

        click(show_in_button_pattern, region=local_directory_row_region)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        if OSHelper.is_mac():
            type(text='o', modifier=KeyModifier.CMD)
            time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/3)
            type('g', modifier=[KeyModifier.CMD, KeyModifier.SHIFT])
            time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT / 3)
            paste('safebrowsing/google4')
            type(Key.ENTER)
            time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT / 3)
            type('a', modifier=KeyModifier.CMD)
            time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT / 3)
            type(Key.BACKSPACE, modifier=KeyModifier.CMD)
        elif OSHelper.is_mac():
            type('l', modifier=KeyModifier.CTRL)
            time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT / 3)
            paste('safebrowsing/google4')
            type(Key.ENTER)
            time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT / 3)
            type('a', modifier=KeyModifier.CTRL)
            time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT / 3)
            type(Key.DELETE)
        else:
            type('d', modifier=KeyModifier.ALT)
            time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT / 3)
            type(Key.RIGHT)
            paste('\\safebrowsing\\google4')
            type(Key.ENTER)
            time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT / 3)
            type('a', modifier=KeyModifier.CTRL)
            time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT / 3)
            type(Key.DELETE)
            time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT / 3)
            type(Key.ENTER)

        close_window_control('auxiliary')

        restore_firefox_focus()

        navigate('about:url-classifier')

        url_classifier_page_opened = exists(url_classifier_title_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert url_classifier_page_opened is True, 'URL Classifier page is successfully opened'

        open_find()

        paste('Cache')

        providers_displays = exists(google4_row_pattern, Settings.FIREFOX_TIMEOUT)
        assert providers_displays, 'The providers are displayed'

        google4_row_location = find(google4_row_pattern)
        google4_row_width, google4_row_height = google4_row_pattern.get_size()
        google4_row_region = Region(google4_row_location.x, google4_row_location.y,
                                    Screen.SCREEN_WIDTH - google4_row_location.x, google4_row_height)

        click(trigger_update_button_pattern, region=google4_row_region)

        quit_firefox()

        firefox.start()

        navigate('about:url-classifier')

        url_classifier_page_opened = exists(url_classifier_title_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert url_classifier_page_opened is True, 'URL Classifier page is successfully opened'

        open_find()

        paste('Cache')

        providers_displays = exists(google4_row_pattern, Settings.FIREFOX_TIMEOUT)
        assert providers_displays, 'The providers are displayed'

        google4_row_location = find(google4_row_pattern)
        google4_row_width, google4_row_height = google4_row_pattern.get_size()
        google4_row_region = Region(google4_row_location.x, google4_row_location.y,
                                    Screen.SCREEN_WIDTH - google4_row_location.x, google4_row_height)

        click(trigger_update_button_pattern, region=google4_row_region)

        success_status_displayed = exists(success_status_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT,
                                          google4_row_region)
        assert success_status_displayed, 'Safe browsing v4 DB is updated.'
