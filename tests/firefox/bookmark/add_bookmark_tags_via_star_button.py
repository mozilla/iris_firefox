# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Tags can be added to bookmarks using the star-shaped button.',
        locale=['en-US'],
        test_case_id='163405',
        test_suite_id='2525'
    )
    def run(self, firefox):
        bookmark_button_pattern = LocationBar.STAR_BUTTON_UNSTARRED
        tags_field = Bookmarks.StarDialog.TAGS_FIELD
        done = Bookmarks.StarDialog.DONE
        moz_tagged_bookmark = Pattern('moz_sidebar_bookmark.png')

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        mozilla_page_assert = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_page_assert is True, 'Mozilla page loaded successfully.'

        try:
            wait(bookmark_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('Bookmark star is present on the page.')
            click(bookmark_button_pattern)
        except FindError:
            raise FindError('Bookmark star is not present on the page, aborting.')

        page_bookmarked_assert = exists(Bookmarks.StarDialog.NEW_BOOKMARK, FirefoxSettings.FIREFOX_TIMEOUT)
        assert page_bookmarked_assert is True, 'The page was successfully bookmarked via star button.'

        try:
            wait(tags_field, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('Tags field can be edit.')
            click(tags_field)
        except FindError:
            raise FindError('Tags field is NOT present on the page, aborting.')

        paste('Iris')

        try:
            wait(done, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('Done button is present on the page.')
            click(done)
        except FindError:
            raise FindError('Done button is NOT present on the page.')

        bookmarks_sidebar('open')

        paste('Iris')

        tagged_bookmark_assert = exists(moz_tagged_bookmark, FirefoxSettings.FIREFOX_TIMEOUT)
        assert tagged_bookmark_assert is True, 'Moz bookmark has been successfully tagged.'
