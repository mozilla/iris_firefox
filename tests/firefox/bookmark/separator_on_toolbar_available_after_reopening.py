# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bug 1461685 - The Bookmarks Toolbar is displayed empty ' \
                    'after creating a separator before its first bookmark',
        locale=['en-US'],
        test_case_id='171344',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        most_visited_toolbar_bookmarks_folder_pattern = Pattern('most_visited_bookmarks.png')
        new_separator_option_pattern = Pattern('new_separator_option.png')
        toolbar_separator_pattern = Pattern('toolbar_separator.png')
        toolbar_bookmarks_pattern = Pattern('toolbar_bookmarks.png')

        open_bookmarks_toolbar()

        toolbar_enabled = exists(most_visited_toolbar_bookmarks_folder_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert toolbar_enabled is True, 'The Bookmarks Toolbar is successfully enabled.'

        location_of_most_visited_folder = find(most_visited_toolbar_bookmarks_folder_pattern)
        region_with_separator = Region(location_of_most_visited_folder.x-5, location_of_most_visited_folder.y-5, 50, 50)

        right_click(most_visited_toolbar_bookmarks_folder_pattern)

        new_separator_option_available = exists(new_separator_option_pattern)
        assert new_separator_option_available is True, '\'New separator\' option available in context menu after' \
                                                       ' right click at item in Bookmarks Toolbar'

        click(new_separator_option_pattern)

        separator_appeared = exists(toolbar_separator_pattern, region=region_with_separator)
        assert separator_appeared is True, 'A separator is placed in front of the first bookmark/folder ' \
                                           'inside the Bookmark Toolbar.'

        open_bookmarks_toolbar()  # to close the toolbar

        try:
            toolbar_disabled = wait_vanish(most_visited_toolbar_bookmarks_folder_pattern)
            assert toolbar_disabled is True, 'The Bookmark Toolbar is no longer displayed.'
        except FindError:
            raise FindError('Toolbar did not close')

        open_bookmarks_toolbar()

        bookmarks_displayed_properly = exists(toolbar_bookmarks_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmarks_displayed_properly is True, 'Toolbar opened. All the bookmarks/folders are in the proper ' \
                                                     'place, like were previously set. Note: In the affected build ' \
                                                     'the Bookmarks Toolbar was completely empty after re-enabled.'

        separator_appeared = exists(toolbar_separator_pattern, region=region_with_separator)
        assert separator_appeared  is True, 'Separator available on toolbar after reopening'
