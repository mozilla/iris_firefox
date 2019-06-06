# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Websites can be bookmarked via URL drag & drop onto the Bookmarks Sidebar.',
        locale=['en-US'],
        test_case_id='168923',
        test_suite_id='2525'
    )
    def run(self, firefox):
        draggable_url_pattern = Pattern('moz_draggable_url.png').similar(.6)
        drag_area_pattern = Pattern('drag_area_moz.png')
        moz_bookmark_pattern = Pattern('moz_sidebar_bookmark.png')
        bookmark_selected_pattern = LocationBar.STAR_BUTTON_STARRED
        sidebar_bookmarks_pattern = SidebarBookmarks.BOOKMARKS_TOOLBAR_MENU

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        mozilla_page_assert = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_page_assert is True, 'Mozilla page loaded successfully.'

        bookmarks_sidebar('open')

        try:
            wait(sidebar_bookmarks_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('Bookmarks section can be accessed.')
            click(sidebar_bookmarks_pattern)
        except FindError:
            raise FindError('Bookmarks section is not present on the page, aborting.')

        select_location_bar()

        draggable_url_exists = exists(draggable_url_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert draggable_url_exists is True, 'Draggable url is present on the screen'

        drag_drop(draggable_url_pattern, SidebarBookmarks.BOOKMARKS_TOOLBAR_MENU, duration=2)

        star_shaped_button_assert = exists(bookmark_selected_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert star_shaped_button_assert is True, 'Star-shaped button has changed its color to blue.'

        bookmarked_url_assert = exists(moz_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmarked_url_assert is True, 'Moz page has been successfully bookmarked via URL onto the ' \
                                              'Bookmarks Sidebar'
