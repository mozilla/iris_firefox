# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This test case checks that one-off searches are displayed in the awesome bar.'

    def run(self):
        url = LocalWeb.FIREFOX_TEST_SITE
        one_off_searches = 'one_off_searches.png'
        search_settings = 'search_settings.png'
        moz = 'moz.png'

        region = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        select_location_bar()
        paste('moz')

        expected = region.exists(moz, 10)
        assert_true(self, expected, 'Searched string found at the bottom of the drop-down list.')

        expected = region.exists(search_settings, 10)
        assert_true(self, expected, 'The \'Search settings\' button is displayed in the awesome bar.')

        expected = region.exists(one_off_searches, 10)
        assert_true(self, expected, 'The one-off searches are displayed in the awesome bar.')
