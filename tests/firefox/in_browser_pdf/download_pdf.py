# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.firefox_ui.helpers.download_manager_utils import downloads_cleanup
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='PDF files can be successfully downloaded via pdf.js.',
        locales=['en-US'],
        test_case_id='3932',
        test_suite_id='65',
        preferences={'browser.download.dir': PathManager.get_downloads_dir(),
                     'browser.download.useDownloadDir': True,
                     'browser.download.folderList': 2,
                     }
    )
    def run(self, firefox):
        pdf_in_downloads_pattern = Pattern('pdf_document_filename_in_downloads.png')
        download_pdf_button_pattern = Pattern('download_button_pdf_viewer.png')
        first_page_contents_pattern = Pattern('pdf_file_page_contents.png')

        change_preference('pdfjs.defaultZoomValue', '100')

        pdf_file_path = self.get_asset_path('pdf.pdf')
        navigate(pdf_file_path)

        pdf_opened = exists(first_page_contents_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert pdf_opened, 'PDF file successfully opened in pdf.js'

        download_button_available = exists(download_pdf_button_pattern)
        assert download_button_available, '\'Download\' button available in pdf.js'

        click(download_pdf_button_pattern)

        save_file_dialog_exists = exists(DownloadDialog.SAVE_FILE_RADIOBUTTON, FirefoxSettings.FIREFOX_TIMEOUT)
        assert save_file_dialog_exists is True, '\'Save file\' dialog opened'

        # "Save file" radio button is selected by default.
        # An additional click is performed to be completely sure that it actually is.
        click(DownloadDialog.SAVE_FILE_RADIOBUTTON)

        ok_button_exists = exists(DownloadDialog.OK_BUTTON, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert ok_button_exists, '\'OK\' button available in \'Save file\' dialog'

        click(DownloadDialog.OK_BUTTON)

        restore_firefox_focus()

        open_downloads()

        downloads_menu_opened = exists(Library.DOWNLOADS, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert downloads_menu_opened, 'Downloads menu opened'

        # Move mouse to the center of the screen to prevent pdf_in_downloads_pattern to be overlapped by any tooltip
        move(Location(Screen().SCREEN_WIDTH // 2, Screen().SCREEN_HEIGHT // 2))

        pdf_listed_in_downloads_section = exists(pdf_in_downloads_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert pdf_listed_in_downloads_section, 'Downloaded PDF document is listed in Library\'s \'Downloads\' section'

        downloads_dir = PathManager.get_downloads_dir()
        file_present_in_filesystem = 'pdf.pdf' in os.listdir(downloads_dir)
        assert file_present_in_filesystem, 'File successfully saved into a filesystem'

    def teardown(self):
        downloads_cleanup()

        if exists(Library.TITLE, 0.5):
            click_window_control('close')

        if exists(NavBar.HOME_BUTTON, 0.5):
            restore_firefox_focus()
            quit_firefox()
