# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that checks the zoom controls on location bar.'

    def run(self):
        url = 'en.wikipedia.org'
        search_bar_wikipedia_default_zoom_level = 'search_bar_wikipedia_default_zoom_level.png'
        hamburger_menu = 'hamburger_menu.png'
        search_bar_wikipedia_110_zoom_level = 'search_bar_wikipedia_110%_zoom_level.png'
        search_bar_wikipedia_300_zoom_level = 'search_bar_wikipedia_300%_zoom_level.png'
        search_bar_wikipedia_30_zoom_level = 'search_bar_wikipedia_30%_zoom_level.png'
        search_bar_wikipedia_90_zoom_level = 'search_bar_wikipedia_90%_zoom_level.png'

        navigate(url)

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

        restart_firefox(self.app.fx_path, self.profile, url='en.wikipedia.org')

        expected = exists(search_bar_wikipedia_110_zoom_level, 10)
        assert_true(self, expected, 'Zoom controls still displayed in the url bar after browser restart.')

        zoom_out()

        expected = exists(search_bar_wikipedia_default_zoom_level, 10)
        assert_true(self, expected, 'Zoom level successfully decreased, zoom controls not found in the url bar for 100% zoom level.')

        restart_firefox(self.app.fx_path, self.profile, url='en.wikipedia.org')

        expected = exists(search_bar_wikipedia_default_zoom_level, 10)
        assert_true(self, expected, 'Zoom controls not found in the url bar after browser restart for 100% zoom level.')

        for i in range(8):
            zoom_in()
            time.sleep(0.5)

        expected = exists(search_bar_wikipedia_300_zoom_level, 10)
        assert_true(self, expected, 'Zoom level successfully increased, maximum zoom level(300%) reached.')

        zoom_in()

        expected = exists(search_bar_wikipedia_300_zoom_level, 10)
        assert_true(self, expected, 'Zoom level still displays 300%.')

        for i in range(8):
            zoom_out()
            time.sleep(0.5)

        expected = exists(search_bar_wikipedia_default_zoom_level, 10)
        assert_true(self, expected, 'Zoom level successfully decreased, zoom controls not found in the url bar for 100% zoom level.')

        for i in range(5):
            zoom_out()
            time.sleep(0.5)
            if i == 0:
                if Settings.getOS() == Platform.LINUX:
                    expected = exists(search_bar_wikipedia_90_zoom_level, 10, 0.99)
                    assert_true(self, expected, 'Zoom level successfully decreased to 90%.')
                else:
                    expected = exists(search_bar_wikipedia_90_zoom_level, 10)
                    assert_true(self, expected, 'Zoom level successfully decreased to 90%.')

        expected = exists(search_bar_wikipedia_30_zoom_level, 10)
        assert_true(self, expected, 'Zoom level successfully decreased, minimum zoom level(30%) reached.')

        zoom_out()

        expected = exists(search_bar_wikipedia_30_zoom_level, 10)
        assert_true(self, expected, 'Zoom level still displays 30%.')
