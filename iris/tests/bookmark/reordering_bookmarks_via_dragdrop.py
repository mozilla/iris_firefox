# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Bug 1391166 - Reordering of Bookmarks via Drag&Drop is incorrect'
        self.test_case_id = '171598'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        library_mozilla_firefox_folder_pattern = Pattern('library_mozilla_firefox_folder.png')
        mozilla_about_us_bookmark_pattern = Pattern('library_about_us_bookmark.png')
        customize_firefox_bookmark_pattern = Pattern('library_customize_firefox_bookmark.png')
        get_involved_bookmark_pattern = Pattern('library_get_involved_bookmark.png')
        help_and_tutorials_bookmark_pattern = Pattern('library_help_and_tutorials_bookmark.png')
        help_and_tutorial_first_line_pattern = Pattern('help_and_tutorial_first_line.png')

        open_library()

        library_opened = exists(Library.TITLE, Settings.FIREFOX_TIMEOUT)
        assert_true(self, library_opened, 'Library is opened')

        bookmark_menu_folder_exists = exists(Library.BOOKMARKS_MENU)
        assert_true(self, bookmark_menu_folder_exists, 'Bookmark menu folder exists')

        bookmark_menu_folder_location = find(Library.BOOKMARKS_MENU)
        bookmark_menu_folder_width, bookmark_menu_folder_height = Library.BOOKMARKS_MENU.get_size()
        bookmarks_tree_region = Region(bookmark_menu_folder_location.x, bookmark_menu_folder_location.y,
                                       bookmark_menu_folder_width, bookmark_menu_folder_height*4)

        double_click(Library.BOOKMARKS_MENU)

        mozilla_firefox_folder_exists = exists(library_mozilla_firefox_folder_pattern, in_region=bookmarks_tree_region)
        assert_true(self, mozilla_firefox_folder_exists, 'Mozilla Firefox folder exists')

        click(library_mozilla_firefox_folder_pattern, in_region=bookmarks_tree_region)

        mozilla_customize_firefox_bookmark_exists = exists(customize_firefox_bookmark_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, mozilla_customize_firefox_bookmark_exists, 'Customize Firefox bookmark is displayed')

        mozilla_get_involved_bookmark_exists = exists(get_involved_bookmark_pattern)
        assert_true(self, mozilla_get_involved_bookmark_exists, 'Get Involved bookmark is displayed')

        mozilla_help_and_tutorials_bookmark_exists = exists(help_and_tutorials_bookmark_pattern)
        assert_true(self, mozilla_help_and_tutorials_bookmark_exists, 'Help and Tutorials bookmark is displayed')

        mozilla_about_us_bookmark_exists = exists(mozilla_about_us_bookmark_pattern)
        assert_true(self, mozilla_about_us_bookmark_exists, 'About Us bookmark is displayed')

        help_and_tutorials_location = find(help_and_tutorials_bookmark_pattern)
        help_and_tutorials_width, help_and_tutorials_height = help_and_tutorials_bookmark_pattern.get_size()
        first_bookmark_region = Region(help_and_tutorials_location.x, help_and_tutorials_location.y,
                                       help_and_tutorials_width, help_and_tutorials_height)

        second_bookmark_region = Region(help_and_tutorials_location.x,
                                        help_and_tutorials_location.y + help_and_tutorials_height,
                                        help_and_tutorials_width, int(help_and_tutorials_height/0.8))

        location_to_drop = find(get_involved_bookmark_pattern)

        click(mozilla_about_us_bookmark_pattern)

        type(Key.DELETE)

        help_and_tutorial_bookmark_position = exists(help_and_tutorial_first_line_pattern)
        assert_true(self, help_and_tutorial_bookmark_position, 'Help and tutorial bookmark is placed on the first line')

        drag_drop(help_and_tutorials_location, location_to_drop)

        click(library_mozilla_firefox_folder_pattern)

        mozilla_customize_firefox_bookmark_exists = exists(customize_firefox_bookmark_pattern, Settings.FIREFOX_TIMEOUT,
                                                           first_bookmark_region)
        assert_true(self, mozilla_customize_firefox_bookmark_exists, 'Customize Firefox bookmark is placed on the first'
                                                                     ' line after replacing Help and tutorial by drag '
                                                                     'and drop to the second line')

        help_and_tutorials_bookmark_replaced = exists(help_and_tutorials_bookmark_pattern,
                                                      in_region=second_bookmark_region)
        assert_true(self, help_and_tutorials_bookmark_replaced, 'Help and tutorial is placed on the second line. '
                                                                'Get Involved is placed on the third line')

        close_window_control('auxiliary')
