# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="This is a test of the Print dialog controls.",
        locale=["en-US"],
        test_case_id="118804",
        test_suite_id="1998"
    )
    def run(self, firefox):
        test_pdf_pattern = Pattern("moz_fast.png")
        print_button_pattern = Pattern("pdf_print_button.png")
        dialog_pattern = Pattern("print_dialog.png")

        navigate(PathManager.get_web_asset_dir("moz.pdf"))

        pdf_found = exists(test_pdf_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert pdf_found, "The test PDF couldn't open"

        click(print_button_pattern)
        print_dialog_found = exists(dialog_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert print_dialog_found, "Print dialog is not present in test pdf."

        if OSHelper.is_mac():
            click_cancel_button()
        elif OSHelper.get_os_version() == "win7":
            type(Key.ESC)
        else:
            click_window_control("close")

        try:
            assert wait_vanish(dialog_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT), "Print dialog was closed."
        except FindError:
            raise FindError("Print dialog is still present.")
