# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='The name of a bookmark can be changed.',
        locale=['en-US'],
        test_case_id='163400',
        test_suite_id='2525'
    )
    def run(self, firefox):
        done_pattern = Bookmarks.StarDialog.DONE
        modified_bookmark_pattern = Pattern('moz_modified_bookmark.png')
        modified_bookmark_2_pattern = Pattern('moz_modified_bookmark_2.png')
        properties_pattern = Pattern('properties_option.png')
        save_pattern = Pattern('save_bookmark_name.png')
        toolbar_bookmark_pattern = Pattern('moz_toolbar_bookmark.png')
        modified_toolbar_bookmark_pattern = Pattern('moz_modified_toolbar_bookmark.png')
        view_bookmarks_toolbar_pattern = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_TOOLBAR

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        mozilla_page_assert = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_page_assert is True, 'Mozilla page loaded successfully.'

        bookmark_page()

        time.sleep(FirefoxSettings.FIREFOX_TIMEOUT/10)

        paste('iris')

        button_assert = exists(done_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert button_assert is True, 'Changes can be saved.'

        click(done_pattern)
        bookmarks_sidebar('open')

        paste('iris')

        bookmark_name_assert = exists(modified_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmark_name_assert is True, 'The name of the bookmark is successfully modified.'

        right_click(modified_bookmark_pattern)

        option_assert = exists(properties_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert option_assert is True, 'Properties option is present on the page.'

        click(properties_pattern)

        properties_window_assert = exists(save_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert properties_window_assert is True, 'Properties window is present on the page.'

        paste('iris_sidebar')

        click(save_pattern)

        bookmark_name_sidebar = exists(modified_bookmark_2_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmark_name_sidebar is True, 'The name of the bookmark is successfully modified.'

        access_bookmarking_tools(view_bookmarks_toolbar_pattern)

        drag_drop(modified_bookmark_2_pattern, Pattern('drag_area.png'), duration=0.5)

        navigate('about:blank')
        bookmarks_sidebar('close')

        toolbar_bookmark_assert = exists(toolbar_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert toolbar_bookmark_assert is True, 'Name of the bookmark can be changed from the toolbar.'

        right_click(toolbar_bookmark_pattern)

        option_assert = exists(properties_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert option_assert is True, 'Properties option is present on the page.'

        click(properties_pattern)

        properties_window_assert = exists(save_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert properties_window_assert is True, 'Properties window is present on the page.'

        paste('iris_toolbar')

        click(save_pattern)

        bookmark_name_toolbar = exists(modified_toolbar_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmark_name_toolbar is True, 'The name of the bookmark is successfully modified.'
