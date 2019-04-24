# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Bug 1467102 - Attempting to download from ftp://ftp causes a hang.'
        self.test_case_id = '179119'
        self.test_suite_id = '1827'
        self.locales = ['en-US']

    def setup(self):
        """Test case setup

        This overrides the setup method in the BaseTest class, so that it can use a brand new profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.BRAND_NEW
        self.set_profile_pref({'browser.download.dir': IrisCore.get_downloads_dir()})
        self.set_profile_pref({'browser.download.folderList': 2})
        self.set_profile_pref({'browser.download.useDownloadDir': True})
        return

    def run(self):

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

        expected = exists(DownloadFiles.DOWNLOADS_PANEL_FREETDS_PATCHED, 90)
        assert_true(self, expected, 'The \'freetds-patched\' file is successfully downloaded.')

    def teardown(self):
        # Remove downloads folder
        downloads_cleanup()
