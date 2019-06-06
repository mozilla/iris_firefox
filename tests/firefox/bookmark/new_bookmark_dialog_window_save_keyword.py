# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bug 1440644 - The New Bookmark dialog/window doesn\'t save the keyword',
        locale=['en-US'],
        test_case_id='171599',
        test_suite_id='2525'
    )
    def run(self, firefox):
        soap_bookmark_pattern = Pattern('soap_bookmark.png').similar(.6)
        new_bookmark_window_pattern = Pattern('new_bookmark_window.png')
        keyword_suggestion_pattern = Pattern('keyword_suggestion.png').similar(.7)
        add_button_pattern = Pattern('add_button.png')

        open_library()

        library_opened = exists(Library.TITLE, FirefoxSettings.FIREFOX_TIMEOUT)
        assert library_opened is True, 'Library opened'

        other_bookmarks_folder_exists = exists(Library.OTHER_BOOKMARKS)
        assert other_bookmarks_folder_exists is True, 'Other Bookmarks folder exists'

        other_bookmarks_width, other_bookmarks_height = Library.OTHER_BOOKMARKS.get_size()
        location_for_right_click = find(Library.OTHER_BOOKMARKS).right(other_bookmarks_width * 2)

        right_click(location_for_right_click)

        new_bookmark_option_exists = exists(Library.Organize.NEW_BOOKMARK)
        assert new_bookmark_option_exists is True, 'New Bookmark option exists'

        click(Library.Organize.NEW_BOOKMARK)

        new_bookmark_window_opened = exists(new_bookmark_window_pattern)
        assert new_bookmark_window_opened is True, 'New Bookmark window is displayed'

        paste('SOAP')
        type(Key.TAB)

        paste(LocalWeb.SOAP_WIKI_TEST_SITE)
        type(Key.TAB)

        paste('SOAP')
        if OSHelper.is_mac():
            type(Key.TAB)
        else:
            type(Key.TAB)
            type(Key.TAB)
        paste('y')

        add_button_active = exists(add_button_pattern)
        assert add_button_active is True, 'The fields are properly filled and the Add button is active and highlighted.'

        click(add_button_pattern)

        bookmark_exists = exists(soap_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmark_exists is True, 'The new bookmark is added in the selected section'

        click(Library.TITLE)

        close_window_control('auxiliary')

        select_location_bar()

        type('y')

        suggestion_exists = exists(keyword_suggestion_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert suggestion_exists is True, 'The keyword search displays as first suggestion the bookmarked website.'
