# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Warnings are displayed if unsafe websites are accessed or downloads initiated.',
        locale=['en-US'],
        test_case_id='219580',
        test_suite_id='3063',
        preferences={'browser.download.dir': PathManager.get_downloads_dir(),
                     'browser.download.folderList': 2,
                     'browser.download.useDownloadDir': True},
        blocked_by={'id': '3460', 'platform': OSPlatform.WINDOWS}
    )
    def run(self, firefox):
        url_classifier_title_pattern = Pattern('url_classifier_title.png')
        google4_row_pattern = Pattern('google4_row.png')
        trigger_update_button_pattern = Pattern('trigger_update_button.png')
        success_status_pattern = Pattern('success_status.png')
        desktop_download_warning_title_pattern = Pattern('desktop_download_warning_title.png')
        first_test_label_pattern = Pattern('first_test_label.png').similar(0.6)
        link_pattern = Pattern('link_image.png').similar(0.6)
        google_row_pattern = Pattern('google_row.png')
        mozilla_row_pattern = Pattern('mozilla_row.png')
        save_file_button_pattern = Pattern('save_file_button.png')

        navigate('about:url-classifier')

        url_classifier_page_opened = exists(url_classifier_title_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert url_classifier_page_opened is True, 'URL Classifier page is successfully opened'

        open_find()

        paste('Cache')

        providers_displays = exists(google4_row_pattern, Settings.FIREFOX_TIMEOUT)
        assert providers_displays is True, 'The providers are displayed'

        google4_row_location = find(google4_row_pattern)
        mozilla_row_location = find(mozilla_row_pattern)
        google4_row_width, google4_row_height = google4_row_pattern.get_size()

        google4_row_region = Screen().new_region(google4_row_location.x, google4_row_location.y,
                                                 Screen.SCREEN_WIDTH-google4_row_location.x, google4_row_height)
        google4_row_region.click(trigger_update_button_pattern)

        google4_success_status_displaying = exists(success_status_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                                                   google4_row_region)
        assert google4_success_status_displaying is True, 'The last google4 update status is changed to success.'

        mozilla_row_region = Screen().new_region(mozilla_row_location.x, mozilla_row_location.y,
                                                 Screen.SCREEN_WIDTH-mozilla_row_location.x, google4_row_height)

        mozilla_row_region.click(trigger_update_button_pattern)

        mozilla_success_status_displaying = exists(success_status_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                                                   mozilla_row_region)
        assert mozilla_success_status_displaying is True, 'The last mozilla update status is changed to success.'

        navigate('http://testsafebrowsing.appspot.com/')

        test_page_opened = exists(desktop_download_warning_title_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert test_page_opened is True, 'The \'testsafebrowsing\' page is properly loaded'

        desktop_download_warning_location = find(desktop_download_warning_title_pattern)
        desktop_download_warning_width, desktop_download_warning_height = desktop_download_warning_title_pattern. \
            get_size()

        desktop_download_warning_region = Screen().new_region(desktop_download_warning_location.x,
                                                              desktop_download_warning_location.y,
                                                              desktop_download_warning_width,
                                                              desktop_download_warning_height)

        first_test_label_width, first_test_label_height = first_test_label_pattern.get_size()
        first_test_label_location = find(first_test_label_pattern, desktop_download_warning_region)

        download_button = find(NavBar.LIBRARY_MENU).left(15)

        coordinate_y = first_test_label_location.y

        for download_tests in range(6):
            region_to_click = Screen().new_region(first_test_label_location.x, coordinate_y,
                                                  Screen.SCREEN_WIDTH-first_test_label_location.x,
                                                  first_test_label_height)

            region_to_click.click(link_pattern)

            if OSHelper.is_windows():
                download_dialog_opened = exists(save_file_button_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
                assert download_dialog_opened is True, 'Download dialog opened'

                click(save_file_button_pattern)
            else:
                download_dialog_opened = exists(DownloadDialog.OK_BUTTON, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
                assert download_dialog_opened is True, 'Download dialog opened'

                click(DownloadDialog.OK_BUTTON)

            coordinate_y += first_test_label_height
            click(download_button)

            downloads_opened = exists(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON)
            assert downloads_opened is True, 'Downloads opened'

            download_completed = exists(DownloadManager.DownloadState.COMPLETED)
            assert download_completed is False, 'File was not downloaded successfully'
