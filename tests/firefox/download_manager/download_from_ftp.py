# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from targets.firefox.firefox_ui.helpers.download_manager_utils import DownloadFiles, downloads_cleanup
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bug 1467102 - Attempting to download from ftp://ftp causes a hang.',
        locale=['en-US'],
        test_case_id='179119',
        test_suite_id='1827',
        profile=Profiles.BRAND_NEW,
        preferences={'browser.download.dir': PathManager.get_downloads_dir(),
                     'browser.download.folderList': 2,
                     'browser.download.useDownloadDir': True,
                     'browser.warnOnQuit': False}
    )
    def run(self, firefox):
        navigate('ftp://ftp.freetds.org/pub/freetds/stable/freetds-patched.tar.gz')

        try:
            wait(DownloadFiles.SAVE_FILE, 90)
            logger.debug('The \'Save file\' option is present in the page.')
            click(DownloadFiles.SAVE_FILE)
        except FindError:
            raise FindError('The \'Save file\' option is not present in the page, aborting.')

        try:
            wait(DownloadFiles.OK, 10)
            logger.debug('The OK button found in the page.')
            click(DownloadFiles.OK)
        except FindError:
            raise FindError('The OK button is not found in the page.')

        expected = exists(NavBar.DOWNLOADS_BUTTON_BLUE, 30)
        assert expected is True, 'Downloads button found.'

        expected = exists(DownloadFiles.DOWNLOADS_PANEL_FREETDS_PATCHED, 90)
        assert expected is True, 'The \'freetds-patched\' file is successfully downloaded.'

    def teardown(self):
        # Remove downloads folder
        downloads_cleanup()
