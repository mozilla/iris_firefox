# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Downloaded files from Private session are successfully saved locally',
        locales=['en-US'],
        test_case_id='101676',
        test_suite_id='1826',
        preferences={'browser.download.dir': PathManager.get_downloads_dir(),
                     'browser.download.folderList': 2,
                     'browser.download.useDownloadDir': True
                     }
    )
    def run(self, firefox):
        first_bytes_label_pattern = Pattern('163_bytes_label.png')
        first_bytes_label_pattern.similar(0.7)
        second_bytes_label_pattern = Pattern('724_bytes_label.png')
        second_bytes_label_pattern.similar(0.7)
        about_downloads_label_pattern = Pattern('about_downloads_label.png')

        new_private_window()
        private_browsing_window_opened = exists(PrivateWindow.private_window_pattern,
                                                FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert private_browsing_window_opened is True, 'Private Browsing Window opened'

        navigate(LocalWeb.SAMPLE_FILES + '1.zip')
        save_file_dialog_exists = exists(DownloadDialog.SAVE_FILE_RADIOBUTTON, FirefoxSettings.FIREFOX_TIMEOUT)
        assert save_file_dialog_exists is True, 'Save file dialog opened'

        click(DownloadDialog.SAVE_FILE_RADIOBUTTON)
        ok_button_exists = exists(DownloadDialog.OK_BUTTON, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert ok_button_exists is True, 'Button OK exists'

        click(DownloadDialog.OK_BUTTON)

        restore_firefox_focus()

        navigate(LocalWeb.SAMPLE_FILES + '2.zip')
        save_file_dialog_exists = exists(DownloadDialog.SAVE_FILE_RADIOBUTTON, FirefoxSettings.FIREFOX_TIMEOUT)
        assert save_file_dialog_exists is True, 'Save file dialog opened'

        click(DownloadDialog.SAVE_FILE_RADIOBUTTON)
        ok_button_exists = exists(DownloadDialog.OK_BUTTON, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert ok_button_exists is True, 'Button OK exists'

        click(DownloadDialog.OK_BUTTON)

        open_downloads()

        about_downloads_label_exists = exists(about_downloads_label_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert about_downloads_label_exists is True, 'Downloads opened'

        if OSHelper.is_mac():
            click(about_downloads_label_pattern)

        first_file_downloaded = exists(first_bytes_label_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert first_file_downloaded is True, 'First file saved'

        second_file_downloaded = exists(second_bytes_label_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert second_file_downloaded is True, 'Second file saved'

        close_window()

        downloads_dir = PathManager.get_downloads_dir()
        PathManager.remove_dir_contents(downloads_dir)
