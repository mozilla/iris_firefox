# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Create \'New Separator\' from \'Bookmarks Toolbar\'',
        locale=['en-US'],
        test_case_id='164370',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        getting_started_toolbar_bookmark_pattern = Pattern('toolbar_bookmark_icon.png')
        new_separator_option_pattern = Pattern('new_separator_option.png')
        bookmark_separator_pattern = Pattern('bookmark_separator.png')

        open_bookmarks_toolbar()

        bookmark_available_in_toolbar = exists(getting_started_toolbar_bookmark_pattern,
                                               FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmark_available_in_toolbar is True, 'The \'Bookmarks Toolbar\' is enabled.'

        right_click(getting_started_toolbar_bookmark_pattern)

        new_separator_option_available = exists(new_separator_option_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert new_separator_option_available is True, '\'New separator\' option is available in context menu after ' \
                                                       'right click at the bookmark'

        click(new_separator_option_pattern)

        try:
            context_menu_closed = wait_vanish(new_separator_option_pattern)
            assert context_menu_closed is True, 'Context menu successfully closed after adding the separator'
        except FindError:
            raise FindError('Context menu didn\'t close after adding the separator for a bookmark')

        separator_added = exists(bookmark_separator_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert separator_added is True, 'A separator is displayed in front of the selected bookmark.'
