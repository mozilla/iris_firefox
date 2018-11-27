# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This test case deletes history from the URL bar completion list.'
        self.test_case_id = '117530'
        self.test_suite_id = '1902'
        self.locales = ['en-US']

    def run(self):
        page_bookmarked_pattern = Bookmarks.StarDialog.NEW_BOOKMARK
        search_suggestion_bookmarked_tab_pattern = Pattern('search_suggestion_bookmarked_tab.png')
        search_suggestion_opened_tab_pattern = Pattern('search_suggestion_opened_tab.png')
        search_suggestion_history_pattern = Pattern('search_suggestion_history.png')
        popular_search_suggestion_pattern = Pattern('popular_search_suggestion.png')
        focus_history_menu_pattern = Pattern('focus_history_menu.png')
        library_menu_pattern = NavBar.LIBRARY_MENU

        region = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)

        # Open some pages to create some history.
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        expected = region.exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, expected, 'Mozilla page loaded successfully.')

        bookmark_page()

        expected = region.exists(page_bookmarked_pattern, 10)
        assert_true(self, expected, 'Page was bookmarked.')

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)
        expected = region.exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Firefox page loaded successfully.')

        new_tab()
        navigate(LocalWeb.FOCUS_TEST_SITE)
        expected = region.exists(LocalWeb.FOCUS_LOGO, 10)
        assert_true(self, expected, 'Focus page loaded successfully.')

        restart_firefox(self,
                        self.browser.path,
                        self.profile_path,
                        LocalWeb.FIREFOX_TEST_SITE,
                        image=LocalWeb.FIREFOX_LOGO)

        new_tab()

        select_location_bar()
        paste('f')

        expected = region.exists(search_suggestion_history_pattern, 10)
        assert_true(self, expected, 'Web pages from personal browsing history found between search suggestions.')

        expected = region.exists(popular_search_suggestion_pattern, 10)
        assert_true(self, expected,
                    'Popular search suggestions from the default search engine found between search suggestions.')

        open_library_menu('History')

        expected = region.exists(focus_history_menu_pattern, 10)
        assert_true(self, expected, 'Focus page displayed in history menu.')

        # Close the library menu.
        click(library_menu_pattern)

        select_location_bar()
        paste('o')

        expected = region.exists(search_suggestion_opened_tab_pattern, 10)
        assert_true(self, expected, 'Opened tab found between search suggestions.')

        select_location_bar()
        paste('m')

        expected = region.exists(search_suggestion_bookmarked_tab_pattern, 10)
        assert_true(self, expected, 'Bookmarked page found between search suggestions.')

        select_location_bar()
        paste('f')

        for i in range(2):
            type(Key.DOWN)

        if Settings.get_os() == Platform.WINDOWS or Settings.get_os() == Platform.LINUX:
            type(Key.DELETE)
        else:
            key_down(Key.SHIFT)
            type(Key.DELETE)
            key_up(Key.SHIFT)

        try:
            expected = region.wait_vanish(search_suggestion_history_pattern, 10)
            assert_true(self, expected, 'Focus page is removed from the list.')
        except FindError:
            raise FindError('Focus page is not removed from the list.')

        open_library_menu('History')

        try:
            expected = region.wait_vanish(focus_history_menu_pattern, 10)
            assert_true(self, expected, 'Focus page successfully removed from the history menu.')
        except FindError:
            raise FindError('Focus page is still displayed in history menu.')
