# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This test case checks that no zoom indicator is displayed in the location bar for the default ' \
                    'zoom level.'

    def run(self):
        url = 'en.wikipedia.org'
        search_bar_wikipedia_default_zoom_level = 'search_bar_wikipedia_default_zoom_level.png'
        hamburger_menu = 'hamburger_menu.png'
        search_bar = 'search_bar.png'

        # Check that no zoom level is displayed in the url bar for the default page opened.
        expected = exists(hamburger_menu, 10)
        assert_true(self, expected, 'Browser successfully opened, hamburger menu found.')

        region = create_region_for_url_bar()

        # Move focus away from the location bar.
        click(Pattern(hamburger_menu).target_offset(-120, 150))

        expected = region.exists(search_bar, 10)
        assert_true(self, expected, 'Zoom level not displayed by default in the url bar.')

        # Check that no zoom level is displayed in the url bar for a new page opened if the zoom level is not changed.
        navigate(url)

        expected = region.exists(search_bar_wikipedia_default_zoom_level, 10)
        assert_true(self, expected, 'Zoom level not displayed by default in the url bar.')
