# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bookmarks can be exported to a HTML file.',
        locale=['en-US'],
        test_case_id='169272',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        export_bookmarks = Pattern('export_bookmarks_to_html.png')
        file_format = Pattern('html_file_format.png')
        import_and_backup_button = Library.IMPORT_AND_BACKUP_BUTTON
        save = Pattern('save_button.png')
        overwrite_save = Pattern('overwrite_save.png')

        navigate('about:blank')

        open_library()

        import_and_backup_assert = exists(import_and_backup_button, FirefoxSettings.FIREFOX_TIMEOUT)
        assert import_and_backup_assert is True, 'Import and Backup button has been found.'

        click(import_and_backup_button)

        try:
            wait(export_bookmarks, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('Export Bookmarks to HTMl file option has been found.')
            click(export_bookmarks)
        except FindError:
            raise FindError('Export Bookmarks to HTMl file option is not present on the page, aborting.')

        paste('Iris_Bookmarks')

        save_auxiliary_window_assert = exists(save, FirefoxSettings.FIREFOX_TIMEOUT)
        assert save_auxiliary_window_assert is True, 'Save auxiliary window is present on the page.'

        click(save)

        if exists(overwrite_save, FirefoxSettings.FIREFOX_TIMEOUT):
            click(overwrite_save)

        file_saved_assert = wait_vanish(file_format, FirefoxSettings.FIREFOX_TIMEOUT)
        assert file_saved_assert is True, 'The HTML file has been successfully saved.'

        click_window_control('close')
