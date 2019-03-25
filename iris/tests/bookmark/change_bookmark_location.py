# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'The location of a bookmark can be changed.'
        self.test_case_id = '4149'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        """Test case setup

        Override the setup method to use a pre-canned bookmarks profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):

        view_bookmarks_toolbar_pattern = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_TOOLBAR
        drag_area_pattern = Pattern('drag_area.png')
        save_pattern = Pattern('save_bookmark_name.png')
        changed_toolbar_bookmark_pattern = Pattern('moz_changed_toolbar_bookmark.png')
        moz_bookmark_pattern = Pattern('moz_sidebar_bookmark.png')
        sidebar_bookmark_location_changed_pattern = Pattern('moz_sidebar_bookmark_location_changed.png').similar(0.6)
        moz_page = Pattern('moz_article_page.png')
        bookmark_changed_location_pattern = Pattern('moz_changed_location_bookmark.png')
        properties_option = Pattern('properties_option.png')

        navigate('about:blank')

        bookmarks_sidebar('open')

        paste('mozilla')

        sidebar_bookmark_assert = exists(moz_bookmark_pattern, 10)
        assert_true(self, sidebar_bookmark_assert, 'Moz bookmark is present in the sidebar.')

        right_click(moz_bookmark_pattern)

        bookmark_options(properties_option)

        properties_window_assert = exists(save_pattern, 10)
        assert_true(self, properties_window_assert, 'Properties window is present on the page.')

        type(Key.TAB)

        paste('https://developer.mozilla.org/en-US/docs/Learn')

        click(save_pattern)

        try:
            wait(sidebar_bookmark_location_changed_pattern)
            logger.debug('Changed bookmark is present in Bookmark sidebar.')
            click(sidebar_bookmark_location_changed_pattern)
        except FindError:
            raise FindError('Can\'t find the bookmark in Bookmark sidebar, aborting.')

        bookmark_location_assert = exists(moz_page, 10)
        assert_true(self, bookmark_location_assert, 'The URL of the bookmark is successfully modified.')

        navigate('about:blank')

        access_bookmarking_tools(view_bookmarks_toolbar_pattern)

        time.sleep(Settings.UI_DELAY_LONG)

        drag_drop(bookmark_changed_location_pattern, drag_area_pattern, 1)

        try:
            wait(changed_toolbar_bookmark_pattern, 10)
            logger.debug('Bookmark is present in Bookmark Toolbar section.')
            right_click(changed_toolbar_bookmark_pattern)
        except FindError:
            raise FindError('Can\'t find the bookmark in Bookmark Toolbar section, aborting.')

        bookmark_options(properties_option)

        properties_window_assert = exists(save_pattern, 10)
        assert_true(self, properties_window_assert, 'Properties window is present on the page.')

        type(Key.TAB)

        paste(LocalWeb.MOZILLA_TEST_SITE)

        click(save_pattern)

        try:
            wait(changed_toolbar_bookmark_pattern, 10)
            logger.debug('Bookmark is present in Bookmark Toolbar section.')
            click(changed_toolbar_bookmark_pattern)
        except FindError:
            raise FindError('Can\'t find the bookmark in Bookmark Toolbar section, aborting.')

        mozilla_page_assert = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, mozilla_page_assert, 'The URL has been successfully modified, Moz page loaded successfully.')
