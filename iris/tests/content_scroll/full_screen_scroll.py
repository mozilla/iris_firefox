# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Scrolling works properly while in full screen.'
        self.test_suite_id = '102'
        self.test_case_id = 'C4658'
        self.locale = ['en-US']

    def run(self):
        image_on_page_pattern = Pattern('soap_env_image.png')
        wiki_logo_pattern = Pattern('wiki_logo.png')
        external_links_pattern = Pattern('external_links.png')

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)
        page_loaded = exists(wiki_logo_pattern, DEFAULT_SYSTEM_DELAY)
        assert_true(self, page_loaded, 'Page loaded.')

        full_screen()
        try:
            full_screen_on = wait_vanish(wiki_logo_pattern, DEFAULT_FIREFOX_TIMEOUT)
            assert_true(self, full_screen_on, 'Full screen on')
        except FindError:
            raise FindError('Not entered full screen mode')

        page_content_displayed = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL)
        assert_true(self, page_content_displayed, 'Page content displayed.')
        click(find(LocalWeb.SOAP_WIKI_SOAP_LABEL))  # Clicking pattern may cause link clicking

        # Mouse scroll
        if Settings.is_windows():
            [scroll(-SCREEN_HEIGHT * 10) for _ in range(2)]
        else:
            [scroll(-15) for _ in range(2)]

        mouse_scroll_done = exists(image_on_page_pattern)
        assert_true(self, mouse_scroll_done, 'Mouse scroll down done')

        if Settings.is_windows():
            [scroll(SCREEN_HEIGHT * 10) for _ in range(2)]
        else:
            [scroll(15) for _ in range(2)]

        returned_home_mouse_scroll = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL)
        assert_true(self, returned_home_mouse_scroll, 'Returned to page top using mouse scroll.')

        # arrows scroll
        scroll_down(30)
        arrows_scroll_done = exists(image_on_page_pattern)
        assert_true(self, arrows_scroll_done, 'Arrows scroll done')
        scroll_up(30)
        returned_home_arrows = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL)
        assert_true(self, returned_home_arrows, 'Returned to page top using arrows.')

        # space key scroll
        [page_down() for _ in range(2)]
        arrows_scroll_done = exists(image_on_page_pattern)
        assert_true(self, arrows_scroll_done, '"Space" scroll done')
        [page_up() for _ in range(2)]
        returned_home_shift_space = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL)
        assert_true(self, returned_home_shift_space, 'Returned to page top using "Shift+Space".')

        # page down/up scroll
        [type(Key.PAGE_DOWN) for _ in range(2)]
        page_down_scroll_done = exists(image_on_page_pattern)
        assert_true(self, page_down_scroll_done, '"Space" scroll done')
        [type(Key.PAGE_UP) for _ in range(2)]
        returned_home_page_up = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL)
        assert_true(self, returned_home_page_up, 'Returned to page top using "Page Up".')

        # Ctrl(Cmd)+arrow scroll
        if not Settings.is_mac():
            type(Key.DOWN, KeyModifier.CTRL)

        page_bottom_reached = exists(external_links_pattern)
        assert_true(self, page_bottom_reached, '"Ctrl+Down" scroll done')

        if not Settings.is_mac():
            type(Key.UP, KeyModifier.CTRL)
        returned_home_ctrl_up = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL)
        assert_true(self, returned_home_ctrl_up, 'Returned to page top using "Ctrl+Up".')
