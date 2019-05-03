# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = '[win & linux] Bug 1397387 - No longer able to edit bookmark item after  closing New Bookmark ' \
                    'or New Bookmark Folder dialog by [x] button'
        self.test_case_id = '171452'
        self.test_suite_id = '2525'
        self.locales = ['en-US']
        self.exclude = [Platform.MAC]

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS

    def run(self):
        getting_started_toolbar_bookmark_pattern = Pattern('getting_started_in_toolbar.png')
        new_bookmark_option_pattern = Pattern('new_bookmark_option.png')
        new_bookmark_window_pattern = Pattern('new_bookmark_window.png')
        toolbar_new_bookmark_pattern = Pattern('new_bookmark.png')
        delete_option_pattern = Pattern('delete_bookmark.png')

        open_bookmarks_toolbar()

        toolbar_opened = exists(getting_started_toolbar_bookmark_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, toolbar_opened, 'The Bookmarks Toolbar is successfully enabled.')

        getting_started_bookmark_location = find(getting_started_toolbar_bookmark_pattern)
        click_location_x_offset = SCREEN_WIDTH // 2
        click_location_y_offset = getting_started_toolbar_bookmark_pattern.get_size()[1] // 2

        getting_started_bookmark_location.offset(click_location_x_offset, click_location_y_offset)

        right_click(getting_started_bookmark_location)

        new_bookmark_option_available = exists(new_bookmark_option_pattern)
        assert_true(self, new_bookmark_option_available,
                    '\'New Bookmark\' option available in context menu after right click at toolbar.')

        click(new_bookmark_option_pattern)

        new_bookmark_popup_opened = exists(new_bookmark_window_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, new_bookmark_popup_opened, 'The \'New Bookmark\' popup window is displayed.')

        close_window_control('auxiliary')

        popup_opened = exists(new_bookmark_window_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_false(self, popup_opened, 'The popup window closes instantly.')

        try:
            new_bookmark_not_created = wait_vanish(toolbar_new_bookmark_pattern, Settings.TINY_FIREFOX_TIMEOUT)
            assert_true(self, new_bookmark_not_created,
                        'New Bookmark is not saved as bookmarked inside the Bookmarks Toolbar.')
        except FindError:
            raise FindError('\'New bookmark\' pattern did not vanish')

        right_click(getting_started_toolbar_bookmark_pattern)

        delete_option_available = exists(delete_option_pattern)
        assert_true(self, delete_option_available,
                    '\'Delete\' option available in context menu after right click at bookmark from toolbar.')

        click(delete_option_pattern)

        getting_started_bookmark_available = exists(getting_started_toolbar_bookmark_pattern)
        assert_false(self, getting_started_bookmark_available,
                     'Delete bookmark action is successfully performed. - Note: In the affected build, '
                     'New Bookmark/ New Folder was displayed as bookmarked inside the Bookmarks Toolbar once the popup '
                     'window was dismissed. No action (delete/rename/move) could be done either, as a consequence of '
                     'closing the popup window via [x] button. ')
