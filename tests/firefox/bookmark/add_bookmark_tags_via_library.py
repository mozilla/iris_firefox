# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Tags can be added to bookmarks using the star-shaped button.',
        locale=['en-US'],
        test_case_id='4146',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        library_bookmarks_pattern = Library.BOOKMARKS_TOOLBAR
        moz_library_pattern = Pattern('moz_library_bookmark.png')
        moz_tagged_bookmark = Pattern('moz_sidebar_bookmark.png')
        tags_field = Bookmarks.StarDialog.TAGS_FIELD

        navigate('about:blank')

        open_library()

        bookmarks_menu_library_assert = exists(library_bookmarks_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmarks_menu_library_assert is True, 'Bookmarks menu has been found.'

        click(library_bookmarks_pattern)

        type(Key.ENTER)
        type(Key.DOWN)

        library_bookmark_assert = exists(moz_library_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert library_bookmark_assert is True, 'Moz bookmark is present in the Library section.'

        click(moz_library_pattern)

        try:
            wait(tags_field, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('Tags field is present on the page.')
            click(tags_field)
        except FindError:
            raise FindError('Tags field is NOT present on the page, aborting.')

        paste('Iris')

        click_window_control('close')

        bookmarks_sidebar('open')

        paste('Iris')

        tagged_bookmark_assert = exists(moz_tagged_bookmark, FirefoxSettings.FIREFOX_TIMEOUT)
        assert tagged_bookmark_assert is True, 'Moz bookmark has been successfully tagged via library.'
