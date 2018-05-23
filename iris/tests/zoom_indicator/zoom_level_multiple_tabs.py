# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that checks the zoom level on multiple tabs for multiple sites and also that' \
                ' decrease/increase of zoom level around the maximum level works correctly.'

    def run(self):
        url_1 = 'en.wikipedia.org'
        url_2 = 'www.amazon.com'
        search_bar_wikipedia_default_zoom_level = 'search_bar_wikipedia_default_zoom_level.png'
        hamburger_menu = 'hamburger_menu.png'
        search_bar_wikipedia_110_zoom_level = 'search_bar_wikipedia_110%_zoom_level.png'
        search_bar_wikipedia_300_zoom_level = 'search_bar_wikipedia_300%_zoom_level.png'

        navigate(url_1)

        expected = exists(hamburger_menu, 10)
        assert_true(self, expected, 'Page successfully loaded, hamburger menu found.')

        coord = find(hamburger_menu)
        x_reg = coord.getX() - 350
        y_reg = coord.getY() - 30

        region = Region(x_reg, y_reg, coord.getX() - x_reg, screen_height / 4)

        expected = region.exists(search_bar_wikipedia_default_zoom_level, 10)
        assert_true(self, expected, 'Zoom level not displayed by default in the url bar.')

        zoom_in()

        expected = exists(search_bar_wikipedia_110_zoom_level, 10)
        assert_true(self, expected, 'Zoom level successfully increased, zoom controls found in the url bar.')

        new_tab()

        navigate(url_1)
        time.sleep(1)

        expected = exists(search_bar_wikipedia_110_zoom_level, 10)
        assert_true(self, expected,
                    'Zoom level still displays 110% in the new tab opened for the site for which the zoom level was set.')

        new_tab()

        navigate(url_2)
        time.sleep(1)

        # Location bar looks the same for both wikipedia and amazon sites.
        # Zoom level set for one site does not propagate to other sites.
        expected = region.exists(search_bar_wikipedia_default_zoom_level, 10)
        assert_true(self, expected, 'Zoom level not displayed in the url bar.')

        for i in range(8):
            zoom_in()
            time.sleep(0.5)

        expected = exists(search_bar_wikipedia_300_zoom_level, 10)
        assert_true(self, expected, 'Zoom level successfully increased, maximum zoom level(300%) reached.')

        zoom_out()
        zoom_in()

        expected = exists(search_bar_wikipedia_300_zoom_level, 10)
        assert_true(self, expected, 'Zoom level successfully increased, maximum zoom level(300%) reached.')
