# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that checks the zoom level using the mousewheel.'

    def run(self):
        url = 'en.wikipedia.org'
        search_bar_wikipedia_110_zoom_level = 'search_bar_wikipedia_110%_zoom_level.png'
        search_bar_wikipedia_300_zoom_level = 'search_bar_wikipedia_300%_zoom_level.png'
        search_bar_wikipedia_30_zoom_level = 'search_bar_wikipedia_30%_zoom_level.png'
        search_bar_wikipedia_default_zoom_level = 'search_bar_wikipedia_default_zoom_level.png'
        search_bar_wikipedia_90_zoom_level = 'search_bar_wikipedia_90%_zoom_level.png'

        navigate(url)
        time.sleep(2)

        # zoom in ONE time.
        zoom_with_mouse_wheel(1, ZoomType.up)

        expected = exists(search_bar_wikipedia_110_zoom_level, 10)
        assert_true(self, expected, 'Zoom level successfully increased, zoom controls found in the url bar.')

        # zoom out ONE time.
        zoom_with_mouse_wheel(1, ZoomType.down)

        expected = exists(search_bar_wikipedia_default_zoom_level, 10)
        assert_true(self, expected, 'Zoom controls not found in the url bar after browser restore its zoom level.')

        # zoom out ONE time.
        zoom_with_mouse_wheel(1, ZoomType.down)

        expected = exists(search_bar_wikipedia_90_zoom_level, 10)
        assert_true(self, expected, 'Zoom level successfully decreased to 90%.')

        # zoom in ONE time.
        zoom_with_mouse_wheel(1, ZoomType.up)

        expected = exists(search_bar_wikipedia_default_zoom_level, 10)
        assert_true(self, expected, 'Zoom controls not found in the url bar after browser restore its zoom level.')

        # zoom in until the maximum zoom level(300%) is reached.
        zoom_with_mouse_wheel(20, ZoomType.up)

        if Settings.getOS() == Platform.WINDOWS:
            expected = exists(search_bar_wikipedia_300_zoom_level, 10, 0.99)
            assert_true(self, expected, 'Zoom level successfully increased, maximum zoom level(300%) reached.')
        else:
            expected = exists(search_bar_wikipedia_300_zoom_level, 10)
            assert_true(self, expected, 'Zoom level successfully increased, maximum zoom level(300%) reached.')

        # zoom in ONE more time.
        zoom_with_mouse_wheel(1, ZoomType.up)

        if Settings.getOS() == Platform.WINDOWS:
            expected = exists(search_bar_wikipedia_300_zoom_level, 10, 0.99)
            assert_true(self, expected, 'Zoom level still displays 300%.')
        else:
            expected = exists(search_bar_wikipedia_300_zoom_level, 10)
            assert_true(self, expected, 'Zoom level still displays 300%.')

        # zoom out until the default zoom level(100%) is reached.
        restore_zoom()

        expected = exists(search_bar_wikipedia_default_zoom_level, 10)
        assert_true(self, expected, 'Zoom controls not found in the url bar after browser restore its zoom level.')

        # zoom out until de minimum zoom level(30%) is reached.
        zoom_with_mouse_wheel(7, ZoomType.down)

        expected = exists(search_bar_wikipedia_30_zoom_level, 10)
        assert_true(self, expected, 'Zoom level successfully decreased, minimum zoom level(30%) reached.')

        # zoom out ONE more time.
        zoom_with_mouse_wheel(1, ZoomType.down)

        if Settings.getOS() == Platform.WINDOWS:
            expected = exists(search_bar_wikipedia_30_zoom_level, 10, 0.99)
            assert_true(self, expected, 'Zoom level still displays 30%.')
        else:
            expected = exists(search_bar_wikipedia_30_zoom_level, 10)
            assert_true(self, expected, 'Zoom level still displays 30%.')
