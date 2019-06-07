# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Create a new folder using star-shaped button',
        locale=['en-US'],
        test_case_id='163404',
        test_suite_id='2525'
    )
    def run(self, firefox):
        bookmark_button_pattern = LocationBar.STAR_BUTTON_UNSTARRED
        choose_option_pattern = Bookmarks.StarDialog.PANEL_OPTION_CHOOSE
        bookmarks_toolbar_option_pattern = Library.BOOKMARKS_TOOLBAR
        new_folder_button_pattern = Bookmarks.StarDialog.NEW_FOLDER
        new_folder_created_pattern = Bookmarks.StarDialog.NEW_FOLDER_CREATED
        done_button_pattern = Bookmarks.StarDialog.DONE
        bookmark_folder_pattern = Pattern('moz_bookmark_folder.png').similar(0.7)
        other_bookmarks_folder_pattern = Pattern('edit_bookmark_folder.png')

        if OSHelper.is_linux():
            new_folder_created_pattern = Pattern('new_folder_created.png')

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        mozilla_page_assert = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_page_assert is True, 'Test page loaded successfully.'

        bookmark_button_assert = exists(bookmark_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmark_button_assert is True, 'Bookmark button present.'

        click(bookmark_button_pattern)

        other_bookmarks_folder_assert = exists(other_bookmarks_folder_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert other_bookmarks_folder_assert is True, 'Other bookmarks folder option present.'

        click(other_bookmarks_folder_pattern)

        choose_option_assert = exists(choose_option_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert choose_option_assert is True, 'Choose option present.'

        click(choose_option_pattern)

        bookmarks_toolbar_option_assert = exists(bookmarks_toolbar_option_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmarks_toolbar_option_assert, 'Bookmarks toolbar option present.'

        click(bookmarks_toolbar_option_pattern)

        new_folder_button_assert = exists(new_folder_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert new_folder_button_assert is True, 'New folder button present.'

        click(new_folder_button_pattern)

        new_folder_created_assert = exists(new_folder_created_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert new_folder_created_assert is True, 'New folder created.'

        paste('moz_bookmark')

        done_button_assert = exists(done_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert done_button_assert is True, 'Done button present.'

        click(done_button_pattern)

        bookmark_folder_assert = exists(bookmark_folder_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmark_folder_assert is True, 'Bookmark folder created successfully.'
