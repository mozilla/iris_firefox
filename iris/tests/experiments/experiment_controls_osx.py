# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'window control experiment'

    def run(self):
        open_browser_console()
        time.sleep(2)

        open_browser_console()

        close_auxiliary_window()

        open_browser_console()

        maximize_auxiliary_window()

        minimize_auxiliary_window(is_full_screen=True)














