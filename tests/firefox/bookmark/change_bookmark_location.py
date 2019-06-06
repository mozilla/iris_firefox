# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='The location of a bookmark can be changed.',
        locale=['en-US'],
        test_case_id='4149',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
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

        sidebar_bookmark_assert = exists(moz_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert sidebar_bookmark_assert is True, 'Moz bookmark is present in the sidebar.'

        right_click(moz_bookmark_pattern)

        click(properties_option)

        properties_window_assert = exists(save_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert properties_window_assert is True, 'Properties window is present on the page.'

        type(Key.TAB)

        paste('https://developer.mozilla.org/en-US/docs/Learn')

        click(save_pattern)

        try:
            wait(sidebar_bookmark_location_changed_pattern)
            logger.debug('Changed bookmark is present in Bookmark sidebar.')
            click(sidebar_bookmark_location_changed_pattern)
        except FindError:
            raise FindError('Can\'t find the bookmark in Bookmark sidebar, aborting.')

        close_content_blocking_pop_up()

        bookmark_location_assert = exists(moz_page, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmark_location_assert is True, 'The URL of the bookmark is successfully modified.'

        navigate('about:blank')

        access_bookmarking_tools(view_bookmarks_toolbar_pattern)

        time.sleep(FirefoxSettings.FIREFOX_TIMEOUT/4)

        drag_drop(bookmark_changed_location_pattern, drag_area_pattern, duration=1)

        try:
            wait(changed_toolbar_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('Bookmark is present in Bookmark Toolbar section.')
            right_click(changed_toolbar_bookmark_pattern)
        except FindError:
            raise FindError('Can\'t find the bookmark in Bookmark Toolbar section, aborting.')

        click(properties_option)

        properties_window_assert = exists(save_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert properties_window_assert, 'Properties window is present on the page.'

        type(Key.TAB)

        paste(LocalWeb.MOZILLA_TEST_SITE)

        click(save_pattern)

        try:
            wait(changed_toolbar_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('Bookmark is present in Bookmark Toolbar section.')
            click(changed_toolbar_bookmark_pattern)
        except FindError:
            raise FindError('Can\'t find the bookmark in Bookmark Toolbar section, aborting.')

        mozilla_page_assert = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_page_assert, 'The URL has been successfully modified, Moz page loaded successfully.'
