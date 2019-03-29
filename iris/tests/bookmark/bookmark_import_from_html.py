# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Bookmarks can be imported from a HTML file.'
        self.test_case_id = '169273'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        library_import_backup_pattern = Library.IMPORT_AND_BACKUP_BUTTON
        library_import_bookmarks_from_html_pattern = Library.ImportAndBackup.IMPORT_BOOKMARKS_FROM_HTML
        sidebar_bookmarks_menu_pattern = SidebarBookmarks.BOOKMARKS_MENU
        test_bookmark_imported_pattern = Pattern('test_bookmark_title.png')
        import_bookmarks_from_html_dropdown_pattern = Pattern('import_bookmarks_from_html_dropdown.png')

        test_bookmarks_path = self.get_asset_path('bookmarks.html')

        open_library()

        library_popup_open = exists(library_import_backup_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, library_popup_open, 'Library is correctly opened.')

        click(library_import_backup_pattern)

        import_button_available = exists(library_import_bookmarks_from_html_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, import_button_available, '"Import bookmarks from HTML" button available')

        click(library_import_bookmarks_from_html_pattern)

        if Settings.is_mac():
            type('g', modifier=KeyModifier.CMD + KeyModifier.SHIFT)  # go to folder
            paste(test_bookmarks_path)
            time.sleep(Settings.TINY_FIREFOX_TIMEOUT)

            type(Key.ENTER)

            open_bookmark_file = exists(import_bookmarks_from_html_dropdown_pattern, Settings.FIREFOX_TIMEOUT)
            assert_true(self, open_bookmark_file, 'Import bookmark menu is displayed')

            click(import_bookmarks_from_html_dropdown_pattern)

        else:
            import_bookmarks_from_html_dropdown = exists(import_bookmarks_from_html_dropdown_pattern,
                                                         Settings.FIREFOX_TIMEOUT)
            assert_true(self, import_bookmarks_from_html_dropdown, 'Import bookmark menu is displayed')

            paste(test_bookmarks_path)
            time.sleep(Settings.TINY_FIREFOX_TIMEOUT)

            type(Key.ENTER)

        sidebar_bookmarks_button = exists(sidebar_bookmarks_menu_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, sidebar_bookmarks_button, 'Sidebar bookmarks button available')

        click(sidebar_bookmarks_menu_pattern)

        test_bookmark_imported = exists(test_bookmark_imported_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, test_bookmark_imported,
                    'The bookmarks are successfully imported and displayed in the Library.')

        close_tab()
