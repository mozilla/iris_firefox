# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Create \'New Bookmark...\' from \'Bookmarks Toolbar\''
        self.test_case_id = '164368'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        getting_started_toolbar_bookmark_pattern = Pattern('toolbar_bookmark_icon.png')
        new_bookmark_option_pattern = Pattern('new_bookmark_option.png')
        location_field_pattern = Pattern('bookmark_location_field.png')
        keyword_field_pattern = Pattern('keyword_field.png')
        new_bookmark_pattern = Pattern('new_bookmark.png')

        open_bookmarks_toolbar()

        bookmark_available_in_toolbar = exists(getting_started_toolbar_bookmark_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, bookmark_available_in_toolbar, 'The \'Bookmarks Toolbar\' is enabled.')

        right_click(getting_started_toolbar_bookmark_pattern)

        new_bookmark_option_available = exists(new_bookmark_option_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, new_bookmark_option_available,
                    '\'New bookmark\' option is available in context menu after right click at the bookmark')

        click(new_bookmark_option_pattern)

        location_field_available = exists(location_field_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, location_field_available, 'A new bookmark window is opened.')

        click(location_field_pattern)

        paste('test')

        tags_field_available = exists(Bookmarks.StarDialog.TAGS_FIELD, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, tags_field_available, '\'Tags\' field is available on the \'New bookmark\' window')

        click(Bookmarks.StarDialog.TAGS_FIELD)

        paste('test')

        keyword_field_available = exists(keyword_field_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, keyword_field_available, '\'Keyword\' field is available on the \'New bookmark\' window')

        click(keyword_field_pattern)

        paste('test')

        type(Key.ENTER)

        bookmark_added = exists(new_bookmark_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, bookmark_added, 'The new bookmark is displayed in the \'Bookmarks Toolbar\' menu.')
