# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Open a bookmark in a New Tab from \'Recent Tags\' section'
        self.test_suite_id = '2525'
        self.test_case_id = '171649'
        self.locale = ['en-US']
        self.exclude = [Platform.MAC]

    def run(self):
        bookmarks_top_menu_pattern = Pattern('bookmarks_top_menu.png')
        pocket_bookmark_top_menu_pattern = Pattern('pocket_bookmark_top_menu.png')
        recent_tags_top_menu_pattern = Pattern('recent_tags_top_menu.png')
        tag_field_pattern = Pattern('tag_field.png')
        tag_item_pattern = Pattern('tag_item.png')
        open_in_new_tab_pattern = Pattern('open_bookmark_in_new_tab.png')

        new_tab()
        navigate(LocalWeb.POCKET_TEST_SITE)
        bookmark_page()
        click(tag_field_pattern)
        paste('test_tag')
        type(Key.ENTER)
        close_tab()

        if Settings.is_windows():
            type(Key.ALT)
        elif Settings.is_linux():
            key_down(Key.ALT)
            time.sleep(0.3)
            key_up(Key.ALT)

        firefox_menu_opened = exists(bookmarks_top_menu_pattern)
        assert_true(self, firefox_menu_opened, 'Firefox top menu is displayed')

        click(bookmarks_top_menu_pattern)
        click(recent_tags_top_menu_pattern)

        tagged_bookmark_saved = exists(tag_item_pattern)
        assert_true(self, tagged_bookmark_saved, 'Bookmarked webpage marked with that specific tag is displayed.')

        click(tag_item_pattern)
        right_click(pocket_bookmark_top_menu_pattern)
        click(open_in_new_tab_pattern)

        page_opened = exists(LocalWeb.POCKET_LOGO)
        assert_true(self, page_opened, 'The selected website is correctly opened')
