# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Create \'New Bookmark...\' from \'Bookmarks Toolbar\'',
        locale=['en-US'],
        test_case_id='164368',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        getting_started_toolbar_bookmark_pattern = Pattern('toolbar_bookmark_icon.png')
        new_bookmark_option_pattern = Pattern('new_bookmark_option.png')
        location_field_pattern = Pattern('bookmark_location_field.png')
        keyword_field_pattern = Pattern('keyword_field.png')
        new_bookmark_pattern = Pattern('new_bookmark.png')

        open_bookmarks_toolbar()

        bookmark_available_in_toolbar = exists(getting_started_toolbar_bookmark_pattern,
                                               FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmark_available_in_toolbar is True, 'The \'Bookmarks Toolbar\' is enabled.'

        right_click(getting_started_toolbar_bookmark_pattern)

        new_bookmark_option_available = exists(new_bookmark_option_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert new_bookmark_option_available  is True,  '\'New bookmark\' option is available in context menu after ' \
                                                        'right click at the bookmark'

        click(new_bookmark_option_pattern)

        location_field_available = exists(location_field_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert location_field_available  is True, 'A new bookmark window is opened.'

        click(location_field_pattern)

        paste('test')

        tags_field_available = exists(Bookmarks.StarDialog.TAGS_FIELD, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert tags_field_available is True, '\'Tags\' field is available on the \'New bookmark\' window'

        click(Bookmarks.StarDialog.TAGS_FIELD)

        paste('test')

        keyword_field_available = exists(keyword_field_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert keyword_field_available  is True, '\'Keyword\' field is available on the \'New bookmark\' window'

        click(keyword_field_pattern)

        paste('test')

        type(Key.ENTER)

        bookmark_added = exists(new_bookmark_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmark_added is True, 'The new bookmark is displayed in the \'Bookmarks Toolbar\' menu.'
