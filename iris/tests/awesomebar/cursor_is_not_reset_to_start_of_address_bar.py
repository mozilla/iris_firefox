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
        # This feature does not work properly on MAC
        self.exclude = Platform.MAC
        self.locales = ['en-US']

    def run(self):
        select_location_bar()
        paste('a.b')

        open_library()
        expected = exists(Library.TITLE, 10)
        assert_true(self, expected, 'The library was opened successfully.')

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
