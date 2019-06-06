# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Websites can be bookmarked by dragging a URL from a *.txt file.',
        locale=['en-US'],
        test_case_id='165205',
        test_suite_id='2525'
    )
    def run(self, firefox):
        link = Pattern('link.png')
        local_link = Pattern('local_link.png')
        selected_local_link = Pattern('selected_local_link.png')
        drag_area = Pattern('drag_area.png')
        view_bookmarks_toolbar = Pattern('view_bookmarks_toolbar.png')
        toolbar_bookmarked_link = Pattern('toolbar_bookmarked_link.png')
        link_page = Pattern('moz_article_page.png')

        test_url = self.get_asset_path('bookmark_link.htm')

        navigate('about:blank')

        access_bookmarking_tools(view_bookmarks_toolbar)

        navigate(test_url)

        link_image_assert = exists(link, FirefoxSettings.FIREFOX_TIMEOUT)
        assert link_image_assert is True, 'Local page is successfully loaded.'

        try:
            wait(local_link, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('The link is present on the page')
            width, height = local_link.get_size()
            location = find(local_link)
            location_from = Location(location.x, location.y + height / 2)
            location_to = Location(location.x + width, location.y + height / 2)
            drag_drop(location_from, location_to, duration=0.2)
        except FindError:
            raise FindError('The link is not present on the page, aborting.')

        try:
            wait(selected_local_link, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('Selected link is present on the page.')
            drag_drop(selected_local_link, SidebarBookmarks.BookmarksToolbar.MOST_VISITED, duration=2)
        except FindError:
            raise FindError('Selected link is not present on the page, aborting.')

        toolbar_link_assert = exists(toolbar_bookmarked_link, FirefoxSettings.FIREFOX_TIMEOUT)
        assert toolbar_link_assert is True, 'The link has been successfully bookmarked.'

        click(toolbar_bookmarked_link)

        close_content_blocking_pop_up()

        link_page_assert = exists(link_page, FirefoxSettings.FIREFOX_TIMEOUT)
        assert link_page_assert is True, 'The page has been successfully loaded.'
