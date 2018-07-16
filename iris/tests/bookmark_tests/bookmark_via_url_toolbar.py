# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'Websites can be bookmarked via URL drag & drop onto the Bookmarks Toolbar.'

    def run(self):
        url = 'about:blank'
        url2 = 'amazon.com'

        draggable_url = 'draggable_url.png'
        toolbar_dragged_bookmark = 'toolbar_dragged_bookmark.png'
        drag_area = 'drag_area.png'
        amazon_home = 'amazon.png'
        bookmarked_star = 'blue_star.png'
        view_bookmarks_toolbar = 'view_bookmarks_toolbar.png'

        navigate(url)

        access_bookmarking_tools(view_bookmarks_toolbar)

        navigate(url2)

        amazon_banner_assert = exists(amazon_home, 10)
        assert_true(self, amazon_banner_assert, 'Amazon page has been successfully loaded.')

        select_location_bar()

        type(Key.ESC)

        drag_drop(draggable_url, drag_area, 0.5)

        star_shaped_button_assert = exists(bookmarked_star, 10)
        assert_true(self, star_shaped_button_assert, 'Star-shaped button has changed its color to blue.')

        navigate(url)

        bookmarked_url_assert = exists(toolbar_dragged_bookmark, 10)
        assert_true(self, bookmarked_url_assert, 'Amazon page has been successfully bookmarked via URL onto '
                                                 'the Bookmarks Toolbar.')
