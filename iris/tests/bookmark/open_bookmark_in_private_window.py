# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Open a bookmark in a New Private Window'
        self.test_case_id = '164366'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        open_in_private_window_option_pattern = Pattern('open_in_private_window_option.png')
        pocket_bookmark_icon_pattern = Pattern('pocket_bookmark_icon.png')
        most_visited_toolbar_bookmark_pattern = Pattern('drag_area.png')

        open_bookmarks_toolbar()

        bookmark_available_in_toolbar = exists(most_visited_toolbar_bookmark_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, bookmark_available_in_toolbar, 'The \'Bookmarks Toolbar\' is enabled.')

        click(most_visited_toolbar_bookmark_pattern)

        pocket_bookmark_available = exists(pocket_bookmark_icon_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, pocket_bookmark_available,
                    '\'Pocket\' bookmark is available in \'Most visited\' folder in toolbar')

        right_click(pocket_bookmark_icon_pattern)

        open_in_private_window_option_available = exists(open_in_private_window_option_pattern,
                                                         DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, open_in_private_window_option_available,
                    '\'Open in Private window\' option is available in context menu after right-click at the bookmark')

        click(open_in_private_window_option_pattern)

        bookmark_opened_in_private_window = exists(PrivateWindow.private_window_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, bookmark_opened_in_private_window, 'The window in which the bookmark is opened is Private')

        page_loaded = exists(LocalWeb.POCKET_IMAGE, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, page_loaded, 'The selected website is correctly opened in a new private window.')

        close_window()
