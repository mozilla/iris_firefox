# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'The name of a bookmark can be changed.'
        self.test_case_id = '163400'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        done_pattern = Bookmarks.StarDialog.DONE
        modified_bookmark_pattern = Pattern('moz_modified_bookmark.png')
        modified_bookmark_2_pattern = Pattern('moz_modified_bookmark_2.png')
        properties_pattern = Pattern('properties_option.png')
        save_pattern = Pattern('save_bookmark_name.png')
        toolbar_bookmark_pattern = Pattern('moz_toolbar_bookmark.png')
        modified_toolbar_bookmark_pattern = Pattern('moz_modified_toolbar_bookmark.png')
        view_bookmarks_toolbar_pattern = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_TOOLBAR

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        mozilla_page_assert = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, mozilla_page_assert, 'Mozilla page loaded successfully.')

        bookmark_page()

        time.sleep(Settings.UI_DELAY)

        paste('iris')

        button_assert = exists(done_pattern, 10)
        assert_true(self, button_assert, 'Changes can be saved.')

        click(done_pattern)
        bookmarks_sidebar('open')

        paste('iris')

        bookmark_name_assert = exists(modified_bookmark_pattern, 10)
        assert_true(self, bookmark_name_assert, 'The name of the bookmark is successfully modified.')

        right_click(modified_bookmark_pattern)

        option_assert = exists(properties_pattern, 10)
        assert_true(self, option_assert, 'Properties option is present on the page.')

        click(properties_pattern)

        properties_window_assert = exists(save_pattern, 10)
        assert_true(self, properties_window_assert, 'Properties window is present on the page.')

        paste('iris_sidebar')

        click(save_pattern)

        bookmark_name_sidebar = exists(modified_bookmark_2_pattern, 10)
        assert_true(self, bookmark_name_sidebar, 'The name of the bookmark is successfully modified.')

        access_bookmarking_tools(view_bookmarks_toolbar_pattern)

        drag_drop(modified_bookmark_2_pattern, Pattern('drag_area.png'), 0.5)

        navigate('about:blank')
        bookmarks_sidebar('close')

        toolbar_bookmark_assert = exists(toolbar_bookmark_pattern, 10)
        assert_true(self, toolbar_bookmark_assert, 'Name of the bookmark can be changed from the toolbar.')

        right_click(toolbar_bookmark_pattern)

        option_assert = exists(properties_pattern, 10)
        assert_true(self, option_assert, 'Properties option is present on the page.')

        click(properties_pattern)

        properties_window_assert = exists(save_pattern, 10)
        assert_true(self, properties_window_assert, 'Properties window is present on the page.')

        paste('iris_toolbar')
        click(save_pattern)

        bookmark_name_toolbar = exists(modified_toolbar_bookmark_pattern, 10)
        assert_true(self, bookmark_name_toolbar, 'The name of the bookmark is successfully modified.')
