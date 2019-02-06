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
        first_test_label_pattern = Pattern('first_test_label.png')
        link_pattern = Pattern('link_image.png')
        download_completed_pattern = Pattern('download_completed.png')

        navigate('about:url-classifier')

        url_classifier_page_opened = exists(url_classifier_title_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, url_classifier_page_opened, 'URL Classifier page is successfully opened')

        open_find()
        paste('Provider')

        google4_row_location = find(google4_row_pattern)
        google4_row_width, google4_row_height = google4_row_pattern.get_size()

        coordinate_y = google4_row_location.y

        for trigger_update in range(3):
            region_to_click = Region(google4_row_location.x, coordinate_y, SCREEN_WIDTH, google4_row_height)
            print(region_to_click)
            click(trigger_update_button_pattern, 0, region_to_click)
            success_status_displaying = exists(success_status_pattern, None, region_to_click)
            if trigger_update == 2:
                assert_false(self, success_status_displaying, 'Nothing changed')
            else:
                assert_true(self, success_status_displaying, 'The last update status changed to success')
            coordinate_y += google4_row_height

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
            download_dialog_opened = exists(DownloadDialog.OK_BUTTON)
            assert_true(self, download_dialog_opened, 'Download dialog opened')
            click(DownloadDialog.OK_BUTTON)
            coordinate_y += first_test_label_height

        click(NavBar.SEVERE_DOWNLOADS_BUTTON)
        time.sleep(DEFAULT_UI_DELAY)
        no_successful_downloads = exists(download_completed_pattern)
        assert_false(self, no_successful_downloads, 'None of the download initiated are successful')
