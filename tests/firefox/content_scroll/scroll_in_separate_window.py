# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description="Scrolling works properly on a website that has been moved to a different window.",
        test_case_id="4657",
        test_suite_id="102",
        locale=["en-US"],
    )
    def run(self, firefox):
        soap_wiki_tab_pattern = Pattern('soap_wiki_tab.png')
        soap_wiki_footer_pattern = Pattern('soap_wiki_footer.png')
        soap_wiki_header_mark_pattern = Pattern('soap_wiki_header.png')
        iris_tab_logo_pattern = Pattern('iris_logo_tab.png').similar(0.75)

        mouse_wheel_steps = 200
        if OSHelper.is_windows():
            mouse_wheel_steps = 1600

        new_tab()

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_test_site_opened = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert soap_wiki_test_site_opened is True, 'The Soap Wiki test site is properly loaded'

        soap_wiki_tab_displayed = exists(soap_wiki_tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert soap_wiki_tab_displayed is True, 'The Soap wiki tab is displayed'

        initial_wiki_tab_location = find(soap_wiki_tab_pattern)

        # Moving Soap Wiki to a new window
        key_down_pressing = 2
        if OSHelper.is_linux():
            key_down_pressing = 1

        right_click(soap_wiki_tab_pattern)

        repeat_key_down(7)
        type(Key.ENTER)
        repeat_key_down(key_down_pressing)
        type(Key.ENTER)

        try:
            soap_wiki_test_site_moved = exists(soap_wiki_tab_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            iris_tab_vanished = wait_vanish(iris_tab_logo_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            assert soap_wiki_test_site_moved is True and iris_tab_vanished is True, 'The Soap Wiki test site ' \
                                                                                    'successfully moved to new window'
        except FindError:
            raise FindError('The Soap Wiki test site is not moved to new window')

        click(LocalWeb.SOAP_WIKI_SOAP_LABEL)

        # Scrolling test in the new window
        # Scroll by mouse wheel
        scroll_by_mouse_wheel_to_footer = scroll_until_pattern_found(soap_wiki_footer_pattern,
                                                                     Mouse().scroll, (None, -mouse_wheel_steps))
        assert scroll_by_mouse_wheel_to_footer is True, 'Successfully scrolled to footer by mouse scroll'

        scroll_by_mouse_wheel_to_header = scroll_until_pattern_found(soap_wiki_header_mark_pattern,
                                                                     Mouse().scroll, (None, mouse_wheel_steps))
        assert scroll_by_mouse_wheel_to_header is True, 'Successfully scrolled to header by mouse scroll'

        # Scroll by pressing arrows
        scroll_by_arrows_to_footer = scroll_until_pattern_found(soap_wiki_footer_pattern, repeat_key_down, (30,))
        assert scroll_by_arrows_to_footer is True, 'Successfully scrolled to footer by pressing arrows'

        scroll_by_arrows_to_header = scroll_until_pattern_found(soap_wiki_header_mark_pattern, repeat_key_up, (30,))
        assert scroll_by_arrows_to_header is True, 'Successfully scrolled to header by pressing arrows'

        # Scroll by pressing Page Up/Page Down
        scroll_by_page_down_to_footer = scroll_until_pattern_found(soap_wiki_footer_pattern, page_down, (None,))
        assert scroll_by_page_down_to_footer is True, 'Successfully scrolled to footer by pressing Page Down'

        scroll_by_page_up_to_header = scroll_until_pattern_found(soap_wiki_header_mark_pattern, page_up, (None,))
        assert scroll_by_page_up_to_header is True, 'Successfully scrolled to header by pressing Page Up'

        # Scroll by pressing Space
        scroll_by_page_down_to_footer = scroll_until_pattern_found(soap_wiki_footer_pattern, type, (Key.SPACE,))
        assert scroll_by_page_down_to_footer is True, 'Successfully scrolled to footer by pressing Space'

        page_home()

        # Scroll by pressing Ctrl+Down/Ctrl+Up or Cmd+Down/Cmd+Up
        if OSHelper.is_mac():
            type(Key.DOWN, modifier=KeyModifier.CMD)
        else:
            type(Key.DOWN, modifier=KeyModifier.CTRL)

        soap_wiki_footer_mark = exists(soap_wiki_footer_pattern)
        assert soap_wiki_footer_mark is True, 'Successfully scrolled to footer by pressing Ctrl+Down or Cmd+Down'

        if OSHelper.is_mac():
            type(Key.UP, modifier=KeyModifier.CMD)
        else:
            type(Key.UP, modifier=KeyModifier.CTRL)

        soap_wiki_header_mark = exists(soap_wiki_header_mark_pattern)
        assert soap_wiki_header_mark is True, 'Successfully scrolled from footer' \
                                              ' to header by pressing Ctrl+Up or Cmd+Up'

        # Move the tab back into initial window
        point_to_move_wiki_window = find(soap_wiki_tab_pattern).right(400)
        location_to_shift_wiki_window = find(soap_wiki_tab_pattern).right(800)
        location_to_shift_wiki_window_linux = find(soap_wiki_tab_pattern).right(2000)

        if OSHelper.is_linux():
            drag_drop(point_to_move_wiki_window, location_to_shift_wiki_window_linux)
        else:
            drag_drop(point_to_move_wiki_window, location_to_shift_wiki_window)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        drag_drop(soap_wiki_tab_pattern, initial_wiki_tab_location)

        click(LocalWeb.SOAP_WIKI_SOAP_LABEL)

        # Scrolling test in the initial window
        # Scroll by mouse wheel
        scroll_by_mouse_wheel_to_footer = scroll_until_pattern_found(soap_wiki_footer_pattern,
                                                                     Mouse().scroll, (None, -mouse_wheel_steps))
        assert scroll_by_mouse_wheel_to_footer is True, 'Successfully scrolled to footer by mouse scroll'

        scroll_by_mouse_wheel_to_header = scroll_until_pattern_found(soap_wiki_header_mark_pattern,
                                                                     Mouse().scroll, (None, mouse_wheel_steps))
        assert scroll_by_mouse_wheel_to_header is True, 'Successfully scrolled to header by mouse scroll'

        # Scroll by pressing arrows
        scroll_by_arrows_to_footer = scroll_until_pattern_found(soap_wiki_footer_pattern, repeat_key_down, (30,))
        assert scroll_by_arrows_to_footer is True, 'Successfully scrolled to footer by pressing arrows'

        scroll_by_arrows_to_header = scroll_until_pattern_found(soap_wiki_header_mark_pattern, repeat_key_up, (30,))
        assert scroll_by_arrows_to_header is True, 'Successfully scrolled to header by pressing arrows'

        # Scroll by pressing Page Up/Page Down
        scroll_by_page_down_to_footer = scroll_until_pattern_found(soap_wiki_footer_pattern, page_down, (None,))
        assert scroll_by_page_down_to_footer is True, 'Successfully scrolled to footer by pressing Page Down'

        scroll_by_page_up_to_header = scroll_until_pattern_found(soap_wiki_header_mark_pattern, page_up, (None,))
        assert scroll_by_page_up_to_header is True, 'Successfully scrolled to header by pressing Page Up'

        # Scroll by pressing Space
        scroll_by_page_down_to_footer = scroll_until_pattern_found(soap_wiki_footer_pattern, type, (Key.SPACE,))
        assert scroll_by_page_down_to_footer, 'Successfully scrolled to footer by pressing Space'

        page_home()

        # Scroll by pressing Ctrl+Down/Ctrl+Up or Cmd+Down/Cmd+Up
        if OSHelper.is_mac():
            type(Key.DOWN, modifier=KeyModifier.CMD)
        else:
            type(Key.DOWN, modifier=KeyModifier.CTRL)

        soap_wiki_footer_mark_initial = exists(soap_wiki_footer_pattern)
        assert soap_wiki_footer_mark_initial is True, 'Successfully scrolled to footer by ' \
                                                      'pressing Ctrl+Down or Cmd+Down'

        if OSHelper.is_mac():
            type(Key.UP, modifier=KeyModifier.CMD)
        else:
            type(Key.UP, modifier=KeyModifier.CTRL)

        soap_wiki_header_mark_initial = exists(soap_wiki_header_mark_pattern)
        assert soap_wiki_header_mark_initial is True, 'Successfully scrolled from footer' \
                                                      ' to header by pressing Ctrl+Up or Cmd+Up'
