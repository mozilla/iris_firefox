# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bookmark a page from the bookmarks menu.',
        locale=['en-US'],
        test_case_id='165474',
        test_suite_id='2525'
    )
    def run(self, firefox):
        bookmark_this_page_pattern = Pattern('bookmark_this_page.png')

        navigate(LocalWeb.FIREFOX_TEST_SITE)

        firefox_logo_exists = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert firefox_logo_exists is True, 'Website is properly loaded'

        library_button_exists = exists(NavBar.LIBRARY_MENU)
        assert library_button_exists is True, '\'View history, saved bookmarks and more\' button exists'

        click(NavBar.LIBRARY_MENU)

        bookmarks_menu_option_exists = exists(LibraryMenu.BOOKMARKS_OPTION)
        assert bookmarks_menu_option_exists is True, 'Bookmarks menu option exists'

        click(LibraryMenu.BOOKMARKS_OPTION)

        star_button_unstarred_exists = exists(LocationBar.STAR_BUTTON_UNSTARRED)
        assert star_button_unstarred_exists is True, 'Unstarred star-shaped button exists'

        bookmark_menu_is_displayed = exists(bookmark_this_page_pattern)
        assert bookmark_menu_is_displayed is True, 'The Bookmarks menu is correctly displayed'

        click(bookmark_this_page_pattern)

        star_button_starred_exists = exists(LocationBar.STAR_BUTTON_STARRED)
        assert star_button_starred_exists is True, 'Star-shaped button changed its color to blue'

        bookmarks_menu_option_exists = exists(LibraryMenu.BOOKMARKS_OPTION)
        assert bookmarks_menu_option_exists is False, 'Bookmarks menu is dismissed'

        star_panel_exists = exists(Bookmarks.StarDialog.NEW_BOOKMARK, FirefoxSettings.FIREFOX_TIMEOUT)
        assert star_panel_exists is True, 'Page Bookmarked menu is displayed under the star-shaped button.'

        click(LocationBar.STAR_BUTTON_STARRED)

        try:
            star_panel_not_exists = wait_vanish(Bookmarks.StarDialog.NEW_BOOKMARK, FirefoxSettings.FIREFOX_TIMEOUT)
            assert star_panel_not_exists is True, 'Page Bookmarked menu is auto dismissed if no action is taken ' \
                                                  'and if the cursor outside the star-panel. '
        except FindError:
            raise FindError('Page Bookmarked menu isn\'t auto dismissed')
