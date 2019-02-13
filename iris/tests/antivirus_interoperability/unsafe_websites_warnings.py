# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = "Warnings are displayed if unsafe websites are accessed or downloads initiated."
        self.test_case_id = "219583"
        self.test_suite_id = "3036"
        self.locale = ["en-US"]

    def run(self):
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

        url_classifier_page_opened = exists(url_classifier_title_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, url_classifier_page_opened, 'URL Classifier page is successfully opened')

        open_find()
        paste('Provider')

        providers_displays = exists(google4_row_pattern)
        assert_true(self, providers_displays, 'The providers are displayed')

        google4_row_location = find(google4_row_pattern)
        google_row_location = find(google_row_pattern)
        mozilla_row_location = find(mozilla_row_pattern)
        google4_row_width, google4_row_height = google4_row_pattern.get_size()

        google4_row_region = Region(google4_row_location.x, google4_row_location.y, SCREEN_WIDTH, google4_row_height)
        click(trigger_update_button_pattern, 0, google4_row_region)

        google4_success_status_displaying = exists(success_status_pattern, None, google4_row_region)
        assert_true(self, google4_success_status_displaying, 'The last google4 update status is changed to success.')

        google_row_region = Region(google_row_location.x, google_row_location.y, SCREEN_WIDTH, google4_row_height)
        click(trigger_update_button_pattern, 0, google_row_region)

        google_success_status_displaying = exists(success_status_pattern, None, google_row_region)
        assert_false(self, google_success_status_displaying, 'Nothing changes in the google update status.')

        mozilla_row_region = Region(mozilla_row_location.x, mozilla_row_location.y, SCREEN_WIDTH, google4_row_height)
        click(trigger_update_button_pattern, 0, mozilla_row_region)

        mozilla_success_status_displaying = exists(success_status_pattern, None, mozilla_row_region)
        assert_true(self, mozilla_success_status_displaying, 'The last mozilla update status is changed to success.')

        navigate('http://testsafebrowsing.appspot.com/')

        test_page_opened = exists(desktop_download_warning_title_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, test_page_opened, 'The \'testsafebrowsing\' page is properly loaded')

        desktop_download_warning_location = find(desktop_download_warning_title_pattern)
        desktop_download_warning_width, desktop_download_warning_height = desktop_download_warning_title_pattern. \
            get_size()

        desktop_download_warning_region = Region(desktop_download_warning_location.x,
                                                 desktop_download_warning_location.y,
                                                 desktop_download_warning_width,
                                                 desktop_download_warning_height)

        first_test_label_width, first_test_label_height = first_test_label_pattern.get_size()
        print(first_test_label_height)
        first_test_label_location = find(first_test_label_pattern, desktop_download_warning_region)

        coordinate_y = first_test_label_location.y

        for download_tests in range(6):
            region_to_click = Region(first_test_label_location.x, coordinate_y, SCREEN_WIDTH, first_test_label_height)
            print(region_to_click)
            click(link_pattern, 0, region_to_click)

            if Settings.is_windows():
                download_dialog_opened = exists(save_file_button_pattern, DEFAULT_SYSTEM_DELAY)
                assert_true(self, download_dialog_opened, 'Download dialog opened')
                click(save_file_button_pattern)
            else:
                download_dialog_opened = exists(DownloadDialog.OK_BUTTON, DEFAULT_SYSTEM_DELAY)
                assert_true(self, download_dialog_opened, 'Download dialog opened')
                click(DownloadDialog.OK_BUTTON)
            coordinate_y += first_test_label_height

        downloads_location = find(NavBar.SEVERE_DOWNLOADS_BUTTON)
        downloads_region = Region(downloads_location.x - SCREEN_WIDTH / 2, downloads_location.y, SCREEN_WIDTH / 2,
                                  SCREEN_HEIGHT / 2)
        click(NavBar.SEVERE_DOWNLOADS_BUTTON)
        downloads_opened = exists(DownloadManager.Downloads.SHOW_ALL_DOWNLOADS)
        assert_true(self, downloads_opened, 'Downloads opened')
        no_successful_downloads = exists(DownloadManager.DownloadsPanel.OPEN_CONTAINING_FOLDER, None, downloads_region)
        assert_false(self, no_successful_downloads, 'None of the download initiated are successful')
