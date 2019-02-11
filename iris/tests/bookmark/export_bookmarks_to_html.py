# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Bookmarks can be exported to a HTML file.'
        self.test_case_id = '169272'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        """Test case setup

        Override the setup method to use a pre-canned bookmarks profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):

        export_bookmarks = Pattern('export_bookmarks_to_html.png')
        file_format = Pattern('html_file_format.png')
        import_and_backup_button = Library.IMPORT_AND_BACKUP_BUTTON
        save = Pattern('save_button.png')
        overwrite_save = Pattern('overwrite_save.png')

        navigate('about:blank')

        open_library()

        import_and_backup_assert = exists(import_and_backup_button, 10)
        assert_true(self, import_and_backup_assert, 'Import and Backup button has been found.')

        click(import_and_backup_button)

        try:
            wait(export_bookmarks, 10)
            logger.debug('Export Bookmarks to HTMl file option has been found.')
            click(export_bookmarks)
        except FindError:
            raise FindError('Export Bookmarks to HTMl file option is not present on the page, aborting.')

        paste('Iris_Bookmarks')

        save_auxiliary_window_assert = exists(save, 10)
        assert_true(self, save_auxiliary_window_assert, 'Save auxiliary window is present on the page.')

        click(save)

        if exists(overwrite_save, 10):
            click(overwrite_save)

        file_saved_assert = wait_vanish(file_format, 10)
        assert_true(self, file_saved_assert, 'The HTML file has been successfully saved.')

        click_window_control('close')
