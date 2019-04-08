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

        open_bookmarks_toolbar()

        toolbar_opened = exists(getting_started_toolbar_bookmark_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, toolbar_opened, 'The Bookmarks Toolbar is successfully enabled.')

        getting_started_bookmark_location = find(getting_started_toolbar_bookmark_pattern)
        getting_started_bookmark_location.x += 300
        getting_started_bookmark_location.y += 15

        right_click(getting_started_bookmark_location)

        new_bookmark_option_available = exists(new_bookmark_option_pattern)
        assert_true(self, new_bookmark_option_available,
                    '\'New Bookmark\' option available in context menu after right click at toolbar.')

        click(new_bookmark_option_pattern)

        new_bookmark_popup_opened = exists(new_bookmark_window_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, new_bookmark_popup_opened, 'The \'New Bookmark\' popup window is displayed.')
