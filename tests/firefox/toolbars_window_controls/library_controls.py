# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='This is a test of the library window controls.',
        locale=['en-US'],
        test_case_id='120467',
        test_suite_id='1998'
    )
    def run(self, firefox):
        library_title_pattern = Library.TITLE
        open_library()
        assert exists(library_title_pattern, 10), 'The library was opened successfully.'

        if OSHelper.is_mac():
            click_window_control('maximize')
            click_window_control('minimize')
        else:
            click_window_control('maximize')
            if OSHelper.is_windows():
                assert exists(Pattern('library_restore_button.png'), 10), 'The library was maximized successfully.'
            else:
                assert exists(Pattern('restore_button.png'), 10), 'The library was maximized successfully.'
            click_window_control('minimize')

        try:
            assert wait_vanish(library_title_pattern, 10), 'Window successfully minimized.'
        except FindError:
            raise FindError('Window not minimized, aborting test.')

        if OSHelper.is_mac():
            open_library()
        else:
            restore_window_from_taskbar('library_menu')
        assert exists(library_title_pattern, 10), 'The library was restored successfully.'

        click_window_control('close')
        try:
            assert wait_vanish(library_title_pattern, 10), 'The library was closed successfully.'
        except FindError:
            raise FindError('The library didn\'t close successfully.')
