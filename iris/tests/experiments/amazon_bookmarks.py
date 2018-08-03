# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test for adding a website in the bookmarks section'

    def run(self):
        url = 'www.amazon.com'
        amazon_image = 'amazon.png'
        amazon_bookmark_image_1 = 'amazon_bookmark_1.png'
        amazon_bookmark_image_2 = 'amazon_bookmark_2.png'
        library_menu_pattern = NavBar.LIBRARY_MENU

        navigate(url)

        expected_1 = exists(amazon_image, 10)
        assert_true(self, expected_1, 'Find amazon image')

        bookmark_page()

        # Sometimes we need to wait a bit for favicon to be loaded
        type(Key.ENTER)

        # Sometimes we need to wait because UI is animating after
        # bookmark was created and library icon image isn't found
        time.sleep(Settings.UI_DELAY_LONG)

        # Look for new bookmark via library menu button
        click(library_menu_pattern)
        time.sleep(Settings.UI_DELAY)
        type(Key.TAB)
        type(Key.ENTER)
        time.sleep(Settings.UI_DELAY)

        expected_2 = exists(amazon_bookmark_image_1, 10)
        assert_true(self, expected_2, 'Find amazon bookmark 1st image')

        type(Key.ESC)

        # Sometimes we need to wait a bit for favicon to be loaded
        time.sleep(Settings.UI_DELAY_LONG)

        # Look for bookmark in bookmark menu
        bookmarks_sidebar('open')
        paste('amazon')

        expected_3 = exists(Pattern(amazon_bookmark_image_2).similar(0.7), 10)
        assert_true(self, expected_3, 'Find amazon bookmark 2nd image')
