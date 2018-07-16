# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that checks if the Cut context menu option works properly.'

    def run(self):

        amazon_home = 'amazon.png'
        toolbar_bookmark = 'toolbar_dragged_bookmark.png'
        close_sidebar_search = 'close_sidebar_search.png'
        bookmarks_sidebar_menu = 'bookmarks_sidebar_menu.png'
        bookmarks_sidebar_menu_selected = 'bookmarks_sidebar_menu_selected_state.png'

        navigate('www.amazon.com')

        amazon_banner_assert = exists(amazon_home, 10)
        assert_true(self, amazon_banner_assert, 'Amazon page has been successfully loaded.')

        try:
            wait('amazon_favicon.png', 15)
            logger.debug('Page is fully loaded and favicon displayed.')
        except FindError:
            logger.error('Page is not fully loaded, aborting.')
            raise FindError

        bookmark_page()

        navigate('about:blank')

        time.sleep(2)

        access_bookmarking_tools('view_bookmarks_toolbar.png')

        try:
            wait('toolbar_is_active.png', 10)
            logger.debug('Toolbar has been activated.')
        except FindError:
            logger.error('Toolbar can not be activated, aborting.')

        bookmarks_sidebar('open')

        paste('amazon')

        sidebar_bookmark_assert = exists('sidebar_bookmark.png', 10)
        assert_true(self, sidebar_bookmark_assert, 'Bookmark is present inside the sidebar.')

        drag_drop('amazon_draggable.png', 'drag_area.png', 0.5)

        toolbar_bookmark_assert = exists(toolbar_bookmark, 10)
        assert_true(self, toolbar_bookmark_assert, 'Amazon bookmark is present in the Bookmarks Toolbar.')

        right_click(toolbar_bookmark)

        bookmark_options('cut_option.png')

        try:
            wait(close_sidebar_search, 10)
            logger.debug('Close button is present.')
            click(close_sidebar_search)
        except FindError:
            logger.error('Can\'t find the close button')
            raise FindError

        try:
            wait(bookmarks_sidebar_menu, 10)
            logger.debug('Bookmarks sidebar menu is present.')
            click(bookmarks_sidebar_menu)
        except FindError:
            logger.error('Can\'t find the Bookmarks sidebar menu')
            raise FindError

        right_click(bookmarks_sidebar_menu_selected)

        bookmark_options('paste_option.png')

        pasted_bookmark_assertion = exists('sidebar_bookmark_location_changed.png', 10)
        assert_true(self, pasted_bookmark_assertion, 'Bookmark is present into a different directory, cut option works '
                                                     'as expected.')






