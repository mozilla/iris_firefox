# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Forget a page from the History sidebar.'
        self.test_case_id = '120132'
        self.test_suite_id = '2000'
        self.locales = ['en-US']

    def setup(self):
        """Test case setup

        This overrides the setup method in the BaseTest class, so that it can use a brand new profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.BRAND_NEW

        return

    def run(self):
        search_history_box_pattern = Sidebar.HistorySidebar.SEARCH_BOX
        history_today_sidebar_pattern = Sidebar.HistorySidebar.Timeline.TODAY

        left_upper_corner = Region(0, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        # Open a page to create some history.
        new_tab()

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        test_page_loaded = exists(LocalWeb.MOZILLA_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, test_page_loaded, 'Mozilla page loaded successfully.')

        close_tab()

        # Open the History sidebar.
        history_sidebar()

        sidebar_opened = exists(search_history_box_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, sidebar_opened, 'Sidebar was opened successfully.')

        history_today_expanded = exists(history_today_sidebar_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, history_today_expanded, 'Expand history button displayed properly.')

        click(history_today_sidebar_pattern)

        # Forget a page from the History sidebar.
        test_page_added_to_history = left_upper_corner.exists(LocalWeb.MOZILLA_BOOKMARK_SMALL.similar(0.7),
                                                   Settings.FIREFOX_TIMEOUT)
        assert_true(self, test_page_added_to_history, 'Mozilla page is displayed in the History list successfully.')

        right_click(LocalWeb.MOZILLA_BOOKMARK_SMALL)

        type(text='f')

        try:
            test_page_deleted = left_upper_corner.wait_vanish(LocalWeb.MOZILLA_BOOKMARK_SMALL, Settings.FIREFOX_TIMEOUT)
            assert_true(self, test_page_deleted, 'Mozilla page was deleted successfully from the history.')
        except FindError:
            raise FindError('Mozilla page is still displayed in the history.')

        # Check that Mozilla page is not displayed in the Recent History list.
        open_library_menu(LibraryMenu.HISTORY_BUTTON)

        test_page_not_displayed = exists(LocalWeb.MOZILLA_BOOKMARK_SMALL.similar(0.9), Settings.FIREFOX_TIMEOUT)
        assert_false(self, test_page_not_displayed, 'Mozilla page is not displayed in the Recent History list.')
