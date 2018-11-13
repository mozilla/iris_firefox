# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This is a test of the Download dialog controls.'
        self.test_case_id = '118801'
        self.test_suite_id = '1998'
        self.locales = ['en-US']

    def run(self):
        url = self.get_web_asset_path('moz.pdf')
        test_pdf_pattern = Pattern('moz_fast.png')
        download_button_pattern = Pattern('pdf_download_button.png')
        dialog_pattern = Pattern('download_dialog.png')

        navigate(url)

        # Check to make sure the test PDF is loaded, then click the download button.
        expected = exists(test_pdf_pattern, 10)
        assert_true(self, expected, 'The test PDF is present.')
        click(download_button_pattern)

        # Ensure the dialog appears.
        expected = exists(dialog_pattern, 10)
        assert_true(self, expected, 'Download dialog is present.')

        # Close the dialog.
        click_window_control('close')

        try:
            expected = wait_vanish(dialog_pattern, 5)
            assert_true(self, expected, 'Download dialog was closed.')
        except FindError:
            raise FindError('Download dialog is still present.')
