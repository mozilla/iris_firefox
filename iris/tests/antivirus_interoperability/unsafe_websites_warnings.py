# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = "Warnings are displayed if unsafe websites are accessed or downloads initiated."
        self.test_case_id = "219580"
        self.test_suite_id = "3063"
        self.locale = ["en-US"]

    def setup(self):
        BaseTest.setup(self)
        self.set_profile_pref({'browser.download.dir': IrisCore.get_downloads_dir()})
        self.set_profile_pref({'browser.download.folderList': 2})
        self.set_profile_pref({'browser.download.useDownloadDir': True})

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

        url_classifier_page_opened = exists(url_classifier_title_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, url_classifier_page_opened, 'URL Classifier page is successfully opened')

        open_find()

        paste('Cache')

        providers_displays = exists(google4_row_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, providers_displays, 'The providers are displayed')

        google4_row_location = find(google4_row_pattern)
        google_row_location = find(google_row_pattern)
        mozilla_row_location = find(mozilla_row_pattern)
        google4_row_width, google4_row_height = google4_row_pattern.get_size()

        google4_row_region = Region(google4_row_location.x, google4_row_location.y, SCREEN_WIDTH, google4_row_height)
        click(trigger_update_button_pattern, in_region=google4_row_region)

        google4_success_status_displaying = exists(success_status_pattern, Settings.FIREFOX_TIMEOUT,
                                                   in_region=google4_row_region)
        assert_true(self, google4_success_status_displaying, 'The last google4 update status is changed to success.')

        google_row_region = Region(google_row_location.x, google_row_location.y, SCREEN_WIDTH, google4_row_height)

        click(trigger_update_button_pattern, in_region=google_row_region)

        google_success_status_displaying = exists(success_status_pattern, Settings.FIREFOX_TIMEOUT,
                                                  in_region=google_row_region)
        assert_false(self, google_success_status_displaying, 'Nothing changes in the google update status.')

        mozilla_row_region = Region(mozilla_row_location.x, mozilla_row_location.y, SCREEN_WIDTH, google4_row_height)

        click(trigger_update_button_pattern, in_region=mozilla_row_region)

        mozilla_success_status_displaying = exists(success_status_pattern, Settings.FIREFOX_TIMEOUT,
                                                   in_region=mozilla_row_region)
        assert_true(self, mozilla_success_status_displaying, 'The last mozilla update status is changed to success.')

        navigate('http://testsafebrowsing.appspot.com/')

        test_page_opened = exists(desktop_download_warning_title_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, test_page_opened, 'The \'testsafebrowsing\' page is properly loaded')

        desktop_download_warning_location = find(desktop_download_warning_title_pattern)
        desktop_download_warning_width, desktop_download_warning_height = desktop_download_warning_title_pattern. \
            get_size()

        desktop_download_warning_region = Region(desktop_download_warning_location.x,
                                                 desktop_download_warning_location.y,
                                                 desktop_download_warning_width,
                                                 desktop_download_warning_height)

        first_test_label_width, first_test_label_height = first_test_label_pattern.get_size()
        first_test_label_location = find(first_test_label_pattern, desktop_download_warning_region)

        download_button = find(NavBar.LIBRARY_MENU).left(15)

        coordinate_y = first_test_label_location.y

        for download_tests in range(6):
            region_to_click = Region(first_test_label_location.x, coordinate_y, SCREEN_WIDTH, first_test_label_height)

            click(link_pattern, in_region=region_to_click)

            if Settings.is_windows():
                download_dialog_opened = exists(save_file_button_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
                assert_true(self, download_dialog_opened, 'Download dialog opened')

                click(save_file_button_pattern)
            else:
                download_dialog_opened = exists(DownloadDialog.OK_BUTTON, Settings.SHORT_FIREFOX_TIMEOUT)
                assert_true(self, download_dialog_opened, 'Download dialog opened')

                click(DownloadDialog.OK_BUTTON)

            coordinate_y += first_test_label_height
            click(download_button)

            downloads_opened = exists(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON)
            assert_true(self, downloads_opened, 'Downloads opened')

            download_completed = exists(DownloadManager.DownloadState.COMPLETED)
            assert_false(self, download_completed, 'File was not downloaded successfully')

    def teardown(self):
        downloads_cleanup()
