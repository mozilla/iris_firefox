# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description=' Close Firefox browser when updating safebrowsing DB',
        test_case_id='50359',
        test_suite_id='69',
        locale=['en-US'],

    )
    def run(self, firefox):
        url_classifier_title_pattern = Pattern('url_classifier_title.png')
        google4_row_pattern = Pattern('google4_row.png')
        trigger_update_button_pattern = Pattern('trigger_update_button.png')
        success_status_pattern = Pattern('success_status.png')
        upgating_status_pattern = Pattern('upgating_status.png')
        # console_element_picker_pattern = Pattern('console_element_picker.png')

        navigate('about:url-classifier')

        url_classifier_page_opened = exists(url_classifier_title_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert url_classifier_page_opened is True, 'URL Classifier page is successfully opened'

        # open_web_console()
        #
        # web_console_opened = exists(console_element_picker_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        # assert web_console_opened, 'Web Console opened'
        #
        # console_element_picker_location = find(console_element_picker_pattern)
        # console_element_picker_width, console_element_picker_height = console_element_picker_pattern.get_size()
        # console_region = Region(console_element_picker_location.x, console_element_picker_location.y,
        #                         Screen.SCREEN_WIDTH, console_element_picker_height * 5)
        #
        # network_monitor_displayed = exists('Network', FirefoxSettings.SHORT_FIREFOX_TIMEOUT, console_region)
        # assert network_monitor_displayed, 'Network monitor tab displayed'
        #
        # click('Network', region=console_region)
        #
        # time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
        #
        # no_throttling_option_found = exists('No throttling', FirefoxSettings.SHORT_FIREFOX_TIMEOUT, console_region)
        # assert no_throttling_option_found, 'No throttling option found'
        #
        # click('No throttling', region=console_region)
        #
        # time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT / 2)
        #
        # gprs_option_found = exists('GPRS', FirefoxSettings.SHORT_FIREFOX_TIMEOUT, console_region)
        # assert gprs_option_found, 'GPRS option found'
        #
        # click('GPRS', region=console_region)
        #
        # time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT / 2)
        #
        # click(url_classifier_title_pattern)

        open_find()

        paste('Cache')

        providers_displays = exists(google4_row_pattern, Settings.FIREFOX_TIMEOUT)
        assert providers_displays, 'The providers are displayed'

        google4_row_location = find(google4_row_pattern)
        google4_row_width, google4_row_height = google4_row_pattern.get_size()
        google4_row_region = Region(google4_row_location.x, google4_row_location.y,
                                    Screen.SCREEN_WIDTH - google4_row_location.x, google4_row_height)

        click(trigger_update_button_pattern, region=google4_row_region)

        # updating_status_displayed = exists(upgating_status_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT,
        #                                    google4_row_region)
        # assert updating_status_displayed, 'updating_status_displayed'

        firefox.restart(url='about:url-classifier', image=url_classifier_title_pattern)

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
