# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This is a test of the Print dialog controls.'
        self.test_case_id = '118804'
        self.test_suite_id = '1998'
        self.locales = ['en-US']

    def run(self):
        url = self.get_web_asset_path('moz.pdf')
        test_pdf_pattern = Pattern('moz_fast.png')
        print_button_pattern = Pattern('pdf_print_button.png')
        dialog_pattern = Pattern('print_dialog.png')

        navigate(url)

        # Check to make sure the test PDF is loaded, then click the print button.
        expected = exists(test_pdf_pattern, 10)
        assert_true(self, expected, 'The test PDF is present.')
        click(print_button_pattern)

        # Ensure the dialog appears.
        expected = exists(dialog_pattern, 10)
        assert_true(self, expected, 'Print dialog is present.')

        # Close the dialog.
        if Settings.get_os() == Platform.MAC:
            click_cancel_button()
        elif Settings.get_os_version() == 'win7':
            type(Key.ESC)
        else:
            click_window_control('close')

        try:
            expected = wait_vanish(dialog_pattern, 5)
            assert_true(self, expected, 'Print dialog was closed.')
        except FindError:
            raise FindError('Print dialog is still present.')
