# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.api.core.errors import FindError, APIHelperError
from iris.api.core.firefox_ui.download_manager import DownloadManager
from iris.api.core.mouse import click
from iris.api.core.region import wait, exists, Pattern
from iris.api.helpers.general import click_hamburger_menu_option, close_customize_page
from iris.asserts import assert_true


class CustomizePage(object):
    AUTO_HIDE = Pattern('auto_hide.png')


def auto_hide_download_button(self):
    click_hamburger_menu_option('Customize...')

    expected = exists(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON, 10)
    assert_true(self, expected, 'Downloads button found in the \'Customize\' page.')

    click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON)
    try:
        expected = wait(CustomizePage.AUTO_HIDE, 5)
        assert_true(self, expected, 'The auto-hide button found in the page.')
    except FindError:
        raise APIHelperError('The auto-hide button not found in the page.')

    click(CustomizePage.AUTO_HIDE)
    close_customize_page()
