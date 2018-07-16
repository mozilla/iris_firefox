# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This test case checks the zoom indicator animation using the mousewheel.'

    def run(self):
        url = 'en.wikipedia.org'
        hamburger_menu = 'hamburger_menu.png'
        search_bar_wikipedia_110_zoom_level = 'search_bar_wikipedia_110_zoom_level.png'
        search_bar_wikipedia_default_zoom_level = 'search_bar_wikipedia_default_zoom_level.png'
        search_bar_wikipedia_300_zoom_level = 'search_bar_wikipedia_300_zoom_level.png'
        search_bar_wikipedia_30_zoom_level = 'search_bar_wikipedia_30_zoom_level.png'

        navigate(url)

        expected = exists(hamburger_menu, 10)
        assert_true(self, expected, 'Page successfully loaded, hamburger menu found.')

        region = create_region_for_url_bar()

        expected = region.exists(search_bar_wikipedia_default_zoom_level, 10)
        assert_true(self, expected, 'Zoom level not displayed by default in the url bar.')

        restart_firefox(self.app.fx_path, self.profile_path, url='en.wikipedia.org')

        expected = region.exists(search_bar_wikipedia_default_zoom_level, 10)
        assert_true(self, expected, 'Zoom level not displayed by default in the url bar.')

        # zoom in ONE time.
        zoom_with_mouse_wheel(1, ZoomType.IN)

        expected = exists(search_bar_wikipedia_110_zoom_level, 10)
        assert_true(self, expected, 'Zoom level successfully increased, zoom controls found in the url bar.')

        restart_firefox(self.app.fx_path, self.profile_path, url='en.wikipedia.org')

        expected = exists(search_bar_wikipedia_110_zoom_level, 10)
        assert_true(self, expected, 'Zoom level successfully increased, zoom controls found in the url bar.')

        # zoom out ONE time.
        zoom_with_mouse_wheel(1, ZoomType.OUT)

        expected = exists(search_bar_wikipedia_default_zoom_level, 10)
        assert_true(self, expected, 'Zoom controls not found in the url bar after browser restore its zoom level.')

        # zoom in until the maximum zoom level(300%) is reached.
        zoom_with_mouse_wheel(20, ZoomType.IN)

        if Settings.get_os() == Platform.WINDOWS:
            expected = exists(search_bar_wikipedia_300_zoom_level, 10, 0.99)
            assert_true(self, expected, 'Zoom level successfully increased, maximum zoom level(300%) reached.')
        else:
            expected = exists(search_bar_wikipedia_300_zoom_level, 10)
            assert_true(self, expected, 'Zoom level successfully increased, maximum zoom level(300%) reached.')

        # zoom in ONE more time.
        zoom_with_mouse_wheel(1, ZoomType.IN)

        if Settings.get_os() == Platform.WINDOWS:
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
        zoom_with_mouse_wheel(7, ZoomType.OUT)

        expected = exists(search_bar_wikipedia_30_zoom_level, 10)
        assert_true(self, expected, 'Zoom level successfully decreased, minimum zoom level(30%) reached.')

        # zoom out ONE more time.
        zoom_with_mouse_wheel(1, ZoomType.OUT)

        if Settings.get_os() == Platform.WINDOWS:
            expected = exists(search_bar_wikipedia_30_zoom_level, 10, 0.99)
            assert_true(self, expected, 'Zoom level still displays 30%.')
        else:
            expected = exists(search_bar_wikipedia_30_zoom_level, 10)
            assert_true(self, expected, 'Zoom level still displays 30%.')
