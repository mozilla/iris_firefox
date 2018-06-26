# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test of the Download dialog controls'

    def run(self):
        url = self.get_web_asset_path('moz.pdf')
        test_pdf = 'moz_fast.png'
        download_button = 'pdf_download_button.png'
        dialog = 'download_dialog.png'

        navigate(url)

        # Check to make sure the test PDF is loaded, Then click the download button.
        expected = exists(test_pdf, 5)
        assert_true(self, expected, 'The test PDF is present')
        click(download_button)

        # Ensure the dialog appears
        expected = exists(dialog, 5)
        assert_true(self, expected, 'Download dialog is present')

        # Close the dialog
        close_auxiliary_window()

        try:
            expected = waitVanish(dialog, 5)
            assert_true(self, expected, 'Download dialog was closed')
        except:
            raise FindError('Download dialog is still present')
