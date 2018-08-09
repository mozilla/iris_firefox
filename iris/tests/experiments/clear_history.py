# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test for clearing browser history'

    def run(self):
        url = 'https://www.amazon.com'
        amazon_pattern = Pattern('amazon.png')
        amazon_history_pattern = Pattern('amazon_history.png')
        library_history_pattern = Pattern('library_history.png')
        library_clear_history_pattern = Pattern('library_clear_history.png')
        library_menu_pattern = NavBar.LIBRARY_MENU

        navigate(url)

        expected_1 = exists(amazon_pattern, 5)
        assert_true(self, expected_1, 'Wait for Amazon image to appear')

        click(library_menu_pattern)

        library_menu_assert = exists(library_history_pattern, 5)
        assert_true(self, library_menu_assert, 'Library menu opened and history button is present')

        click(library_history_pattern)
        clear_history_assert = exists(library_clear_history_pattern, 5)
        assert_true(self, clear_history_assert, 'Clear history button is present')

        click(library_clear_history_pattern)

        time.sleep(Settings.UI_DELAY)
        type(Key.ENTER)

        # Because of a Mac bug with the keyboard shortcut for clear history,
        # we want to make sure that we are not in the minimized window state,
        # and that we have returned to a normal Firefox window
        expected_2 = exists(amazon_pattern, 5)
        assert_true(self, expected_2, 'Still viewing the Amazon page')

        # The click here is required, because the Firefox window loses
        # focus after invoking the above dialog, and without it,
        # the keyboard shortcuts don't work

        click(NavBar.HOME_BUTTON)

        # Navigate to new page; otherwise, our bitmap for the history item
        # looks identical to the image in the title bar and we'll get
        # a false match
        navigate('about:blank')

        expected_3 = exists(amazon_pattern, 3)
        assert_false(self, expected_3, 'Successfully re-navigated page')

        history_sidebar()
        time.sleep(Settings.UI_DELAY_LONG)
        type('amazon')

        expected_4 = exists(amazon_history_pattern, 5)
        assert_false(self, expected_4, 'Find amazon history image')
