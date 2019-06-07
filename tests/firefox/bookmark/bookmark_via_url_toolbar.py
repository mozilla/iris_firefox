# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Websites can be bookmarked via URL drag & drop onto the Bookmarks Toolbar.',
        locale=['en-US'],
        test_case_id='4090',
        test_suite_id='2525'
    )
    def run(self, firefox):
        url = 'about:blank'
        draggable_url_pattern = Pattern('moz_draggable_url.png')
        toolbar_dragged_bookmark_pattern = Pattern('moz_toolbar_dragged_bookmark.png')
        drag_area_pattern = Pattern('drag_area.png')
        view_bookmarks_toolbar_pattern = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_TOOLBAR
        bookmark_selected_pattern = LocationBar.STAR_BUTTON_STARRED

        navigate(url)

        access_bookmarking_tools(view_bookmarks_toolbar_pattern)

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        mozilla_page_assert = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_page_assert is True, 'Mozilla page loaded successfully.'

        select_location_bar()

        type(Key.ESC)

        drag_drop(draggable_url_pattern, drag_area_pattern, duration=0.5)

        star_shaped_button_assert = exists(bookmark_selected_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert star_shaped_button_assert is True, 'Star-shaped button has changed its color to blue.'

        navigate(url)

        bookmarked_url_assert = exists(toolbar_dragged_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmarked_url_assert is True, 'Moz page has been successfully bookmarked via URL onto the ' \
                                              'Bookmarks Toolbar.'
