# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Scrolling works properly while in full screen.'
        self.test_suite_id = '102'
        self.test_case_id = '4658'
        self.locale = ['en-US']

    def run(self):
        wiki_logo_pattern = Pattern('wiki_logo.png')
        soap_article_title = Pattern('soap_article_title.png')
        wikimedia_logo_pattern = Pattern('wikimedia_logo.png')
        arrow_scroll_length = 10

        if Settings.is_windows():
            scroll_length = SCREEN_HEIGHT
        elif Settings.is_linux():
            scroll_length = 20
        else:
            scroll_length = 60

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)
        page_loaded = exists(wiki_logo_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, page_loaded, 'Page loaded.')

        full_screen()
        try:
            if Settings.is_mac():
                full_screen_on = wait_vanish(MainWindow.UNHOVERED_MAIN_RED_CONTROL, DEFAULT_FIREFOX_TIMEOUT)
            else:
                full_screen_on = wait_vanish(MainWindow.CLOSE_BUTTON, DEFAULT_FIREFOX_TIMEOUT)
            assert_true(self, full_screen_on, 'Full screen on')
        except FindError:
            raise FindError('Not entered full screen mode')

        page_content_displayed = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, page_content_displayed, 'Page content displayed.')

        click(find(LocalWeb.SOAP_WIKI_SOAP_LABEL))  # Clicking pattern may cause link clicking

        # Mouse scroll
        mouse_scroll_done = scroll_until_pattern_found(wikimedia_logo_pattern, scroll, (-scroll_length,), 20,
                                                       DEFAULT_UI_DELAY)
        assert_true(self, mouse_scroll_done, 'Mouse scroll down done')

        returned_home_mouse_scroll = scroll_until_pattern_found(soap_article_title, scroll, (scroll_length,), 20,
                                                                DEFAULT_UI_DELAY)
        assert_true(self, returned_home_mouse_scroll, 'Returned to page top using mouse scroll.')

        # arrows scroll
        arrows_scroll_done = scroll_until_pattern_found(wikimedia_logo_pattern, scroll_down, (arrow_scroll_length,), 30,
                                                        DEFAULT_UI_DELAY)
        assert_true(self, arrows_scroll_done, 'Arrows scroll done')

        returned_home_arrows = scroll_until_pattern_found(soap_article_title, scroll_up, (arrow_scroll_length,), 30,
                                                          DEFAULT_UI_DELAY)
        assert_true(self, returned_home_arrows, 'Returned to page top using arrows.')

        # space key scroll
        arrows_scroll_done = scroll_until_pattern_found(wikimedia_logo_pattern, type, (Key.SPACE,),
                                                        timeout=DEFAULT_UI_DELAY)
        assert_true(self, arrows_scroll_done, '"Space" scroll done')

        returned_home_shift_space = scroll_until_pattern_found(soap_article_title, type, (Key.SPACE, KeyModifier.SHIFT),
                                                               timeout=DEFAULT_UI_DELAY)
        assert_true(self, returned_home_shift_space, 'Returned to page top using "Shift+Space".')

        # page down/up scroll
        page_down_scroll_done = scroll_until_pattern_found(wikimedia_logo_pattern, type, (Key.PAGE_DOWN,),
                                                           timeout=DEFAULT_UI_DELAY)
        assert_true(self, page_down_scroll_done, '"Space" scroll done')

        returned_home_page_up = scroll_until_pattern_found(soap_article_title, type, (Key.PAGE_UP,),
                                                           timeout=DEFAULT_UI_DELAY)
        assert_true(self, returned_home_page_up, 'Returned to page top using "Page Up".')

        # Ctrl(Cmd)+arrow scroll
        if Settings.is_mac():
            page_bottom_reached = scroll_until_pattern_found(wikimedia_logo_pattern, type,
                                                             (Key.DOWN, KeyModifier.CMD), timeout=DEFAULT_UI_DELAY)
        else:
            page_bottom_reached = scroll_until_pattern_found(wikimedia_logo_pattern, type,
                                                             (Key.DOWN, KeyModifier.CTRL), timeout=DEFAULT_UI_DELAY)
        assert_true(self, page_bottom_reached, '"Ctrl+Down" scroll done')

        if Settings.is_mac():
            returned_home_ctrl_up = scroll_until_pattern_found(soap_article_title, type, (Key.UP, KeyModifier.CMD),
                                                               timeout=DEFAULT_UI_DELAY)
        else:
            returned_home_ctrl_up = scroll_until_pattern_found(soap_article_title, type, (Key.UP, KeyModifier.CTRL),
                                                               timeout=DEFAULT_UI_DELAY)
        assert_true(self, returned_home_ctrl_up, 'Returned to page top using "Ctrl+Up".')
