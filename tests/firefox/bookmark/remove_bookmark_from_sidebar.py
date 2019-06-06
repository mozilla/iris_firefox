# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bookmarks can be removed from the Bookmarks Sidebar.',
        locale=['en-US'],
        test_case_id='168933',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        moz_bookmark_pattern = Pattern('moz_sidebar_bookmark.png')
        delete_pattern = Pattern('delete_bookmark.png')

        navigate('about:blank')

        bookmarks_sidebar('open')

        paste('mozilla')

        try:
            wait(moz_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('Moz bookmark is present in the Bookmark sidebar.')
            right_click(moz_bookmark_pattern)
        except FindError:
            raise FindError('Moz bookmark is NOT present in the Bookmark sidebar, aborting.')

        click(delete_pattern)

        try:
            deleted_bookmark_assert = wait_vanish(moz_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            assert deleted_bookmark_assert, 'Moz bookmark is successfully deleted from the Bookmark sidebar.'
        except FindError:
            raise FindError('Moz bookmark can NOT be deleted from the Bookmark sidebar, aborting.')
