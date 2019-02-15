# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Websites can be bookmarked via URL drag & drop onto the Bookmarks Sidebar.'
        self.test_case_id = '168923'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):

        draggable_url_pattern = Pattern('moz_draggable_url.png')
        drag_area_pattern = Pattern('drag_area_moz.png')
        moz_bookmark_pattern = Pattern('moz_sidebar_bookmark.png')
        bookmark_selected_pattern = LocationBar.STAR_BUTTON_STARRED
        sidebar_bookmarks_pattern = SidebarBookmarks.BOOKMARKS_TOOLBAR_MENU

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        mozilla_page_assert = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, mozilla_page_assert, 'Mozilla page loaded successfully.')

        bookmarks_sidebar('open')

        try:
            wait(sidebar_bookmarks_pattern, 10)
            logger.debug('Bookmarks section can be accessed.')
            click(sidebar_bookmarks_pattern)
        except FindError:
            raise FindError('Bookmarks section is not present on the page, aborting.')

        select_location_bar()

        drag_drop(draggable_url_pattern, drag_area_pattern, 0.5)

        star_shaped_button_assert = exists(bookmark_selected_pattern, 10)
        assert_true(self, star_shaped_button_assert, 'Star-shaped button has changed its color to blue.')

        bookmarked_url_assert = exists(moz_bookmark_pattern, 10)
        assert_true(self, bookmarked_url_assert,
                    'Moz page has been successfully bookmarked via URL onto the Bookmarks Sidebar')
