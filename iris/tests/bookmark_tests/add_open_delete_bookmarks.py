# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a bunch of test cases that checks if the bookmarks can be added, opened or ' \
                    'deleted properly'

    def run(self):
        url = 'www.amazon.com'
        url2 = 'www.bing.com'
        url3 = 'about:home'
        amazon_image = 'amazon.png'
        bing_image = 'bing_home.png'
        star_button = 'bookmark_star.png'
        amazon_bookmark = 'amazon_bookmark.png'
        amazon_library = 'amazon_library.png'
        bing_bookmark = 'bing_bookmark.png'
        highlighted_bing_bookmark = 'highlighted_bing_bookmark.png'
        library_bookmarks = 'library_bookmarks.png'
        delete_bookmark = 'delete_bookmark.png'
        most_visited = 'most_visited_bookmarks.png'
        search_bookmark_1 = 'amazon'
        search_bookmark_2 = 'bing'

        # Test case 139 and 140

        navigate(url)

        expected_1 = exists(amazon_image, 10)
        assert_true(self, expected_1, 'Amazon page has been successfully loaded')

        # Keyboard bookmark

        bookmark_page()

        time.sleep(2)

        navigate(url2)

        expected_2 = exists(bing_image, 10)
        assert_true(self, expected_2, 'Bing page has been successfully loaded')

        # Star button bookmark

        expected_3 = exists(star_button, 10)
        assert_true(self, expected_3, 'Star button exists on the page')

        click(star_button)

        time.sleep(2)

        # Check if the bookmarks exists

        bookmarks_sidebar()
        time.sleep(1)

        paste(search_bookmark_1)

        expected_4 = exists(amazon_bookmark, 10)
        assert_true(self, expected_4, 'Amazon bookmark is present in the sidebar')

        type(Key.ESC)

        paste(search_bookmark_2)

        expected_5 = exists(bing_bookmark, 10)
        assert_true(self, expected_5, 'Bing bookmark is present in the sidebar')

        # Test case 146 - Bookmarks can be opened from the Bookmarks Sidebar

        navigate(url3)

        time.sleep(1)

        click(bing_bookmark)

        expected_6 = exists(bing_image, 10)
        assert_true(self, expected_6, 'Bing bookmark has been successfully accessed from Bookmark Sidebar')

        # Test case 148 - Bookmarks can be opened from the Library
        open_library()

        expected_7 = exists(library_bookmarks, 10)
        assert_true(self, expected_7, 'Bookmarks menu has been found')

        click(library_bookmarks)

        type(Key.ENTER)
        type(Key.DOWN)

        expected_8 = exists(amazon_library, 10)
        assert_true(self, expected_8, 'Amazon bookmark can be accessed in Library section')

        click(amazon_library)
        type(Key.ENTER)

        expected_9 = exists(amazon_image, 10)
        assert_true(self, expected_9, 'Amazon bookmark has been successfully accessed from Library section')

        # Test case 150 - Bookmarks can be removed from the Bookmarks Sidebar

        if Settings.getOS() == Platform.LINUX:
            rightClick(highlighted_bing_bookmark)
        else:
            rightClick(bing_bookmark)

        expected_10 = exists(delete_bookmark, 10)
        assert_true(self, expected_10, 'Bookmark can be deleted')

        click(delete_bookmark)

        try:
            expected_11 = waitVanish(bing_bookmark, 10)
            assert_true(self, expected_11, 'Bing bookmark has been successfully deleted.')
        except Exception as error:
            logger.error('Bing bookmark can not be deleted.')
            raise error

        # Test case 151 - Bookmarks can be removed from the Library

        open_library()

        click(most_visited)

        rightClick(amazon_library)
        click(delete_bookmark)

        try:
            expected_12 = waitVanish(amazon_library, 10)
            assert_true(self, expected_12, 'Amazon bookmark has been successfully deleted.')
        except Exception as error:
            logger.error('Amazon bookmark can not be deleted.')
            raise error
        # Cleanup by closing the Library window
        click_auxiliary_window_control('close')
