# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Drag and drop a bookmark from \'Bookmark Toolbar\''
        self.test_case_id = '164377'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        bookmarks_toolbar_menu_option_pattern = Pattern('bookmarks_toolbar_menu_option.png')
        toolbar_bookmark_pattern = Pattern('toolbar_bookmark_icon.png')
        mozilla_support_logo_pattern = Pattern('mozilla_support_logo.png')
        iris_tab_pattern = Pattern('iris_tab.png')

        area_to_click = find(iris_tab_pattern)
        area_to_click.x += 300
        area_to_click.y += 5
        right_click(area_to_click)

        bookmarks_toolbar_menu_option_available = exists(bookmarks_toolbar_menu_option_pattern, DEFAULT_UI_DELAY)
        assert_true(self, bookmarks_toolbar_menu_option_available,
                    '\'Bookmarks Toolbar\' option is available in context menu')

        click(bookmarks_toolbar_menu_option_pattern)
        bookmark_available_in_toolbar = exists(toolbar_bookmark_pattern, DEFAULT_UI_DELAY)
        assert_true(self, bookmark_available_in_toolbar, 'The \'Bookmarks Toolbar\' is enabled.')

        drag_drop(toolbar_bookmark_pattern, area_to_click)
        select_tab(2)
        bookmarked_website_loaded = exists(mozilla_support_logo_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, bookmarked_website_loaded, 'The selected website is correctly opened.')
