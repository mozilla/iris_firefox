# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Scrolling works properly while in full screen.',
        locale=['en-US'],
        test_case_id='4658',
        test_suite_id='102',
    )
    def run(self, firefox):
        # Our default timeouts during the scroll has to be Settings.TINY_TIMEOUT

        wiki_logo_pattern = Pattern('wiki_logo.png')
        soap_article_title = Pattern('soap_article_title.png')
        wikimedia_logo_pattern = Pattern('wikimedia_logo.png')
        arrow_scroll_length = Screen.SCREEN_HEIGHT/2

        if OSHelper.is_windows():
            scroll_length = Screen.SCREEN_HEIGHT
        elif OSHelper.is_linux():
            scroll_length = 20
        else:
            scroll_length = 200

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        page_loaded = exists(wiki_logo_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert page_loaded is True, 'Page loaded.'

        full_screen()

        try:
            if OSHelper.is_mac():
                full_screen_on = wait_vanish(MainWindow.UNHOVERED_MAIN_RED_CONTROL, FirefoxSettings.FIREFOX_TIMEOUT)
            else:
                full_screen_on = wait_vanish(MainWindow.CLOSE_BUTTON, FirefoxSettings.FIREFOX_TIMEOUT)
            assert full_screen_on is True, 'Full screen on'
        except FindError:
            raise FindError('Not entered full screen mode')

        page_content_displayed = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert page_content_displayed is True, 'Page content displayed.'

        click(find(LocalWeb.SOAP_WIKI_SOAP_LABEL))  # Clicking pattern may cause link clicking

        # Mouse scroll

        mouse_scroll_done = scroll_until_pattern_found(wikimedia_logo_pattern, Mouse().scroll, (0, -scroll_length,), 20,
                                                       timeout=FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
        assert mouse_scroll_done is True, 'Mouse scroll down done'

        returned_home_mouse_scroll = scroll_until_pattern_found(soap_article_title, Mouse().scroll,
                                                                (0, scroll_length,), 20,
                                                                timeout=FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
        assert returned_home_mouse_scroll is True, 'Returned to page top using mouse scroll.'

        # arrows scroll
        arrows_scroll_done = scroll_until_pattern_found(wikimedia_logo_pattern, scroll_down, (arrow_scroll_length,), 30,
                                                        timeout=FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
        assert arrows_scroll_done is True, 'Arrows scroll done'

        returned_home_arrows = scroll_until_pattern_found(soap_article_title, scroll_up, num_of_scroll_iterations=100,
                                                          timeout=FirefoxSettings.TINY_FIREFOX_TIMEOUT/6)
        assert returned_home_arrows is True, 'Returned to page top using arrows.'

        # space key scroll
        arrows_scroll_done = scroll_until_pattern_found(wikimedia_logo_pattern, type, (Key.SPACE,),
                                                        timeout=FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
        assert arrows_scroll_done is True, '"Space" scroll done'

        returned_home_shift_space = scroll_until_pattern_found(soap_article_title, type, (Key.SPACE, KeyModifier.SHIFT),
                                                               timeout=FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
        assert returned_home_shift_space is True, 'Returned to page top using "Shift+Space".'

        # page down/up scroll
        page_down_scroll_done = scroll_until_pattern_found(wikimedia_logo_pattern, type, (Key.PAGE_DOWN,),
                                                           timeout=FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
        assert page_down_scroll_done is True, '"Space" scroll done'

        returned_home_page_up = scroll_until_pattern_found(soap_article_title, type, (Key.PAGE_UP,),
                                                           timeout=FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
        assert returned_home_page_up is True, 'Returned to page top using "Page Up".'

        # Ctrl(Cmd)+arrow scroll
        if OSHelper.is_mac():
            page_bottom_reached = scroll_until_pattern_found(wikimedia_logo_pattern, type,
                                                             (Key.DOWN, KeyModifier.CMD),
                                                             timeout=FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
        else:
            page_bottom_reached = scroll_until_pattern_found(wikimedia_logo_pattern, type,
                                                             (Key.DOWN, KeyModifier.CTRL),
                                                             timeout=FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
        assert page_bottom_reached is True, '"Ctrl+Down" scroll done'

        if OSHelper.is_mac():
            returned_home_ctrl_up = scroll_until_pattern_found(soap_article_title, type, (Key.UP, KeyModifier.CMD),
                                                               timeout=FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
        else:
            returned_home_ctrl_up = scroll_until_pattern_found(soap_article_title, type, (Key.UP, KeyModifier.CTRL),
                                                               timeout=FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
        assert returned_home_ctrl_up is True, 'Returned to page top using "Ctrl+Up".'
