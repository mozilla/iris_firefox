# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Cursor gets reset to start of address bar, when I alt-tab away from Firefox and back.'
        self.test_case_id = '224506'
        self.test_suite_id = '1902'
        self.locales = ['en-US']

    def run(self):
        select_location_bar()
        paste('a.b')

        # MAC acts different from the other supported OSes. Using the change_window_view() helper while having the
        # browser and an auxiliary window from the same browser opened does not move focus from the browser to the
        # auxiliary window and vice-versa. MAC moves focus to a different window(e.g: terminal).
        if Settings.get_os() == Platform.MAC:
            # Move focus away from the browser.
            change_window_view()
            # Move focus back to the browser.
            change_window_view()
        else:
            # Move focus away from the browser by opening an auxiliary window of the browser.
            open_library()
            expected = exists(Library.TITLE, 10)
            assert_true(self, expected, 'The library was opened successfully.')

            # Move focus back to the browser.
            change_window_view()

            try:
                expected = wait_vanish(Library.TITLE, 5)
                assert_true(self, expected, 'The browser is in focus again.')
            except FindError:
                raise FindError('The library is still in focus.')

        paste('test')
        select_location_bar()
        url_text = copy_to_clipboard()
        assert_equal(self, url_text, 'a.btest', 'The cursor did not change its position while the window was changed.')

        if Settings.get_os() == Platform.WINDOWS or Settings.get_os() == Platform.LINUX:
            change_window_view()
            click_window_control('close')
