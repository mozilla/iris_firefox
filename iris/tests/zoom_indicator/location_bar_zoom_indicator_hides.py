# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This test case checks that zoom indicator hides.'

    def run(self):
        url = 'en.wikipedia.org'
        hamburger_menu = 'hamburger_menu.png'
        search_bar_wikipedia_default_zoom_level = 'search_bar_wikipedia_default_zoom_level.png'
        search_bar_wikipedia_110_zoom_level = 'search_bar_wikipedia_110_zoom_level.png'
        search_bar_wikipedia_90_zoom_level = 'search_bar_wikipedia_90_zoom_level.png'

        navigate(url)

        expected = exists(hamburger_menu, 10)
        assert_true(self, expected, 'Page successfully loaded, hamburger menu found.')

        region = create_region_for_url_bar()

        expected = region.exists(search_bar_wikipedia_default_zoom_level, 10)
        assert_true(self, expected, 'Zoom level not displayed by default in the url bar.')

        zoom_in()

        expected = exists(search_bar_wikipedia_110_zoom_level, 10)
        assert_true(self, expected, 'Zoom level successfully increased, zoom controls found in the url bar.')

        zoom_out()

        expected = exists(search_bar_wikipedia_default_zoom_level, 10)
        assert_true(self, expected, 'Zoom level successfully decreased, zoom controls not found in the url bar for 100%'
                                    ' zoom level.')

        zoom_out()

        expected = exists(search_bar_wikipedia_90_zoom_level, 10)
        assert_true(self, expected, 'Zoom level successfully decreased, zoom controls found in the url bar.')

        zoom_in()

        expected = region.exists(search_bar_wikipedia_default_zoom_level, 10)
        assert_true(self, expected, 'Zoom level successfully increased, zoom controls not found in the url bar.')
