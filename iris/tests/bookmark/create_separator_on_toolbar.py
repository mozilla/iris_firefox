# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Create \'New Separator\' from \'Bookmarks Toolbar\''
        self.test_case_id = '164370'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        getting_started_toolbar_bookmark_pattern = Pattern('toolbar_bookmark_icon.png')
        new_separator_option_pattern = Pattern('new_separator_option.png')
        bookmark_separator_pattern = Pattern('bookmark_separator.png')

        open_bookmarks_toolbar()

        bookmark_available_in_toolbar = exists(getting_started_toolbar_bookmark_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, bookmark_available_in_toolbar, 'The \'Bookmarks Toolbar\' is enabled.')

        right_click(getting_started_toolbar_bookmark_pattern)

        new_separator_option_available = exists(new_separator_option_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, new_separator_option_available,
                    '\'New separator\' option is available in context menu after right click at the bookmark')

        click(new_separator_option_pattern)

        try:
            context_menu_closed = wait_vanish(new_separator_option_pattern)
            assert_true(self, context_menu_closed, 'Context menu successfully closed after adding the separator')
        except FindError:
            raise FindError('Context menu didn\'t close after adding the separator for a bookmark')

        separator_added = exists(bookmark_separator_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, separator_added, 'A separator is displayed in front of the selected bookmark.')
