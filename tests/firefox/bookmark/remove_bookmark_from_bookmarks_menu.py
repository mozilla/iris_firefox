# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bookmarks can be removed from Bookmarks menu.',
        locale=['en-US'],
        test_case_id='4101',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        bookmarks_menu_pattern = LibraryMenu.BOOKMARKS_OPTION
        menu_bookmark_pattern = Pattern('moz_bookmark_from_menu.png')
        delete_pattern = Pattern('delete_bookmark.png')

        right_upper_corner = Region(Screen.SCREEN_WIDTH / 2, 0, Screen.SCREEN_WIDTH / 2, Screen.SCREEN_HEIGHT / 2)

        navigate('about:blank')

        open_library_menu(bookmarks_menu_pattern)

        try:
            right_upper_corner.wait(menu_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('Moz bookmark is present in the Bookmarks Menu section.')
            right_click(menu_bookmark_pattern)
        except FindError:
            raise FindError('Moz bookmark is not present in the Bookmarks Menu, aborting.')

        click(delete_pattern)

        try:
            delete_bookmark_menu_assert = right_upper_corner.wait_vanish(menu_bookmark_pattern,
                                                                         FirefoxSettings.FIREFOX_TIMEOUT)
            assert delete_bookmark_menu_assert is True, 'Moz bookmark has been successfully deleted ' \
                                                        'from the Bookmarks Menu.'
        except FindError:
            raise FindError('Moz bookmark can not be deleted from the Bookmarks Menu.')
