# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test of the Download dialog controls'

    def run(self):
        url = 'www.yoanaj.co.il/uploadimages/The_Little_Prince.pdf'
        test_pdf = 'little_prince_sidebar.png'
        download_button = 'pdf_download_button.png'
        dialog = 'download_dialog.png'

        navigate(url)

        # Check to make sure the test PDF is loaded, Then click the download button.
        try:
            wait(test_pdf, 20)
        except:
            raise FindError('Test PDF page not loaded')
        else:
            click(download_button)

        # Ensure the dialog appears
        expected_1 = exists(dialog, 20)
        assert_true(self, expected_1, 'Download dialog is present')

        # Close the dialog
        close_auxiliary_window()

        try:
            expected_2 = waitVanish(dialog, 5)
            assert_true(self, expected_2, 'Download dialog was closed')
        except:
            raise FindError('Download dialog is still present')
