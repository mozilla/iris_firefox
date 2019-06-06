# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Edit a bookmark from the bookmarks menu',
        locale=['en-US'],
        test_case_id='165475',
        test_suite_id='2525'
    )
    def run(self, firefox):
        edit_bookmark_name_before_pattern = Pattern('edit_bookmark_name.png')
        edit_bookmark_name_after_pattern = Pattern('edit_bookmark_name_modified.png')
        edit_bookmark_folder_before_pattern = Pattern('edit_bookmark_folder.png')
        edit_bookmark_folder_after_pattern = Pattern('edit_bookmark_folder_modified.png')
        edit_bookmark_tags_before_pattern = Pattern('tags_before.png')
        edit_bookmark_tags_after_pattern = Pattern('edit_bookmark_tags_modified.png')
        if not OSHelper.is_windows():
            edit_this_bookmark_pattern = Pattern('edit_this_bookmark.png')
        else:
            edit_this_bookmark_pattern = Bookmarks.StarDialog.EDIT_THIS_BOOKMARK

        if OSHelper.is_linux() or OSHelper.is_mac():
            edit_bookmark_folder_option = Pattern('bookmark_menu_folder_option.png')

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        test_site_opened = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert test_site_opened is True, 'Previously bookmarked Mozilla website is opened'

        bookmark_page()

        time.sleep(FirefoxSettings.FIREFOX_TIMEOUT)

        library_button_exists = exists(NavBar.LIBRARY_MENU, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert library_button_exists is True, 'View history, saved bookmarks and more section exists'

        click(NavBar.LIBRARY_MENU)

        bookmarks_menu_option_exists = exists(LibraryMenu.BOOKMARKS_OPTION, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmarks_menu_option_exists is True, 'Bookmarks menu option exists'

        click(LibraryMenu.BOOKMARKS_OPTION)

        edit_this_bookmark_exists = exists(edit_this_bookmark_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert edit_this_bookmark_exists is True, 'The Bookmarks menu is correctly displayed'

        click(edit_this_bookmark_pattern)

        edit_bookmark_title_exists = exists(Bookmarks.StarDialog.EDIT_THIS_BOOKMARK, FirefoxSettings.FIREFOX_TIMEOUT)
        assert edit_bookmark_title_exists is True, 'Edit This Bookmark window is displayed under the star-shaped ' \
                                                   'button from the URL bar'

        edit_bookmark_name_before_exists = exists(edit_bookmark_name_before_pattern,
                                                  FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert edit_bookmark_name_before_exists is True, 'Name field exists'

        edit_bookmark_folder_before_exists = exists(edit_bookmark_folder_before_pattern,
                                                    FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert edit_bookmark_folder_before_exists is True, 'Folder field exists'

        edit_bookmark_tags_before_exists = exists(edit_bookmark_tags_before_pattern,
                                                  FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert edit_bookmark_tags_before_exists is True, 'Tags field exists'

        paste('New Name')

        type(Key.TAB)

        click(edit_bookmark_folder_before_pattern)

        if OSHelper.is_linux() or OSHelper.is_mac():
            edit_bookmark_folder_after_exists = exists(edit_bookmark_folder_option,
                                                       FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
            assert edit_bookmark_folder_after_exists is True, 'Needed option from folder field exists'

            click(edit_bookmark_folder_option)
        else:
            edit_bookmark_folder_after_exists = exists(edit_bookmark_folder_after_pattern,
                                                       FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
            assert edit_bookmark_folder_after_exists is True, 'Needed option from folder field exists'

            click(edit_bookmark_folder_after_pattern)

        click(edit_bookmark_tags_before_pattern)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/3)

        paste('tags, test')

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT / 3)

        type(Key.ENTER)

        library_button_exists = exists(NavBar.LIBRARY_MENU, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert library_button_exists is True, 'View history, saved bookmarks and more section exists'

        click(NavBar.LIBRARY_MENU)

        bookmarks_menu_option_exists = exists(LibraryMenu.BOOKMARKS_OPTION, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmarks_menu_option_exists is True, 'Bookmarks menu option exists'

        click(LibraryMenu.BOOKMARKS_OPTION)

        edit_this_bookmark_exists = exists(edit_this_bookmark_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert edit_this_bookmark_exists is True, 'The Bookmarks menu is correctly displayed'

        click(edit_this_bookmark_pattern)

        edit_bookmark_title_exists = exists(Bookmarks.StarDialog.EDIT_THIS_BOOKMARK, FirefoxSettings.FIREFOX_TIMEOUT)
        assert edit_bookmark_title_exists is True, 'Edit This Bookmark window is displayed under the star-shaped' \
                                                   ' button from the URL bar'

        edit_bookmark_name_after_exists = exists(edit_bookmark_name_after_pattern,
                                                 FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert edit_bookmark_name_after_exists is True, 'Name field was correctly saved'

        edit_bookmark_folder_after_exists = exists(edit_bookmark_folder_after_pattern,
                                                   FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert edit_bookmark_folder_after_exists is True, 'Folder field was correctly saved'

        edit_bookmark_tags_after_exists = exists(edit_bookmark_tags_after_pattern,
                                                 FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert edit_bookmark_tags_after_exists is True, 'Tags field was correctly saved'
