# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = "Scrolling works properly on a website that has been moved to a different window."
        self.test_case_id = "C4657"
        self.test_suite_id = "102"
        self.locale = ["en-US"]

    def run(self):
        soap_wiki_tab_pattern = Pattern('soap_wiki_tab.png')
        soap_wiki_footer_pattern = Pattern('soap_wiki_footer.png')
        soap_wiki_header_mark_pattern = Pattern('soap_wiki_header.png')
        iris_tab_logo_pattern = Pattern('iris_logo_tab.png').similar(0.75)

        mouse_wheel_steps = 100
        if Settings.is_windows():
            mouse_wheel_steps = 1600

        new_tab()
        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_test_site_opened = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, 20)
        assert_true(self, soap_wiki_test_site_opened, 'The Soap Wiki test site is properly loaded')

        # Moving Soap Wiki to a new window
        key_down_pressing = 2
        if Settings.is_linux():
            key_down_pressing = 1

        right_click(soap_wiki_tab_pattern)
        repeat_key_down(7)
        type(Key.ENTER)
        repeat_key_down(key_down_pressing)
        type(Key.ENTER)

        try:
            soap_wiki_test_site_moved = exists(soap_wiki_tab_pattern, 20)
            iris_tab_vanished = wait_vanish(iris_tab_logo_pattern, 20)
            assert_true(self, soap_wiki_test_site_moved and iris_tab_vanished, 'The Soap Wiki test site successfully '
                                                                               'moved to new window')
        except FindError:
            raise FindError('The Soap Wiki test site is not moved to new window')

        click(LocalWeb.SOAP_WIKI_SOAP_LABEL)

        # Scrolling test in the new window
        # Scroll by mouse wheel
        scroll_by_mouse_wheel_to_footer = scroll_until_pattern_found(soap_wiki_footer_pattern,
                                                                     scroll, (-mouse_wheel_steps,))
        assert_true(self, scroll_by_mouse_wheel_to_footer, 'Successfully scrolled to footer by mouse scroll')

        scroll_by_mouse_wheel_to_header = scroll_until_pattern_found(soap_wiki_header_mark_pattern,
                                                                     scroll, (mouse_wheel_steps,))
        assert_true(self, scroll_by_mouse_wheel_to_header, 'Successfully scrolled to header by mouse scroll')

        # Scroll by pressing arrows
        scroll_by_arrows_to_footer = scroll_until_pattern_found(soap_wiki_footer_pattern, repeat_key_down, (30,))
        assert_true(self, scroll_by_arrows_to_footer, 'Successfully scrolled to footer by pressing arrows')

        scroll_by_arrows_to_header = scroll_until_pattern_found(soap_wiki_header_mark_pattern, repeat_key_up, (30,))
        assert_true(self, scroll_by_arrows_to_header, 'Successfully scrolled to header by pressing arrows')

        # Scroll by pressing Page Up/Page Down
        scroll_by_page_down_to_footer = scroll_until_pattern_found(soap_wiki_footer_pattern, page_down, (None,))
        assert_true(self, scroll_by_page_down_to_footer, 'Successfully scrolled to footer by pressing Page Down')

        scroll_by_page_up_to_header = scroll_until_pattern_found(soap_wiki_header_mark_pattern, page_up, (None,))
        assert_true(self, scroll_by_page_up_to_header, 'Successfully scrolled to header by pressing Page Up')

        # Scroll by pressing Space
        scroll_by_page_down_to_footer = scroll_until_pattern_found(soap_wiki_footer_pattern, type, (Key.SPACE,))
        assert_true(self, scroll_by_page_down_to_footer, 'Successfully scrolled to footer by pressing Space')

        page_home()

        # Scroll by pressing Ctrl+Down/Ctrl+Up or Cmd+Down/Cmd+Up
        if Settings.is_mac():
            type(Key.DOWN, modifier=KeyModifier.CMD)
        else:
            type(Key.DOWN, modifier=KeyModifier.CTRL)

        soap_wiki_footer_mark = exists(soap_wiki_footer_pattern)
        assert_true(self, soap_wiki_footer_mark, 'Successfully scrolled to footer by pressing Ctrl+Down or Cmd+Down')

        if Settings.is_mac():
            type(Key.UP, modifier=KeyModifier.CMD)
        else:
            type(Key.UP, modifier=KeyModifier.CTRL)

        soap_wiki_header_mark = exists(soap_wiki_header_mark_pattern)
        assert_true(self, soap_wiki_header_mark, 'Successfully scrolled from footer to header by '
                                                 'pressing Ctrl+Up or Cmd+Up')

        # Move the tab back into initial window
        soap_wiki_new_window_tab_location = find(soap_wiki_tab_pattern)
        location_for_new_window_drop_to_minimize = Location.below(soap_wiki_new_window_tab_location, away_y=500)
        soap_wiki_for_minimize_tab_location = find(soap_wiki_tab_pattern)
        location_for_double_click_to_minimize = Location.right(soap_wiki_for_minimize_tab_location, away_x=500)

        if Settings.is_linux():
            drag_drop(soap_wiki_tab_pattern, location_for_new_window_drop_to_minimize)
        else:
            double_click(location_for_double_click_to_minimize)

        soap_wiki_tab_pattern_to_move = find(soap_wiki_tab_pattern)
        location_to_drop_into_initial_window = Location.right(soap_wiki_tab_pattern_to_move, away_x=1500)

        drag_drop(soap_wiki_tab_pattern, location_to_drop_into_initial_window)

        soap_wiki_test_site_moved_to_initial = exists(soap_wiki_tab_pattern, 20)
        iris_tab_displayed = exists(iris_tab_logo_pattern, 20)
        assert_true(self, soap_wiki_test_site_moved_to_initial and iris_tab_displayed, 'The Soap Wiki test site '
                                                                                       'successfully moved back')
        click(LocalWeb.SOAP_WIKI_SOAP_LABEL)

        # Scrolling test in the initial window
        # Scroll by mouse wheel
        scroll_by_mouse_wheel_to_footer = scroll_until_pattern_found(soap_wiki_footer_pattern,
                                                                     scroll, (-mouse_wheel_steps,))
        assert_true(self, scroll_by_mouse_wheel_to_footer, 'Successfully scrolled to footer by mouse scroll')

        scroll_by_mouse_wheel_to_header = scroll_until_pattern_found(soap_wiki_header_mark_pattern,
                                                                     scroll, (mouse_wheel_steps,))
        assert_true(self, scroll_by_mouse_wheel_to_header, 'Successfully scrolled to header by mouse scroll')

        # Scroll by pressing arrows
        scroll_by_arrows_to_footer = scroll_until_pattern_found(soap_wiki_footer_pattern, repeat_key_down, (30,))
        assert_true(self, scroll_by_arrows_to_footer, 'Successfully scrolled to footer by pressing arrows')

        scroll_by_arrows_to_header = scroll_until_pattern_found(soap_wiki_header_mark_pattern, repeat_key_up, (30,))
        assert_true(self, scroll_by_arrows_to_header, 'Successfully scrolled to header by pressing arrows')

        # Scroll by pressing Page Up/Page Down
        scroll_by_page_down_to_footer = scroll_until_pattern_found(soap_wiki_footer_pattern, page_down, (None,))
        assert_true(self, scroll_by_page_down_to_footer, 'Successfully scrolled to footer by pressing Page Down')

        scroll_by_page_up_to_header = scroll_until_pattern_found(soap_wiki_header_mark_pattern, page_up, (None,))
        assert_true(self, scroll_by_page_up_to_header, 'Successfully scrolled to header by pressing Page Up')

        # Scroll by pressing Space
        scroll_by_page_down_to_footer = scroll_until_pattern_found(soap_wiki_footer_pattern, type, (Key.SPACE,))
        assert_true(self, scroll_by_page_down_to_footer, 'Successfully scrolled to footer by pressing Space')

        page_home()

        # Scroll by pressing Ctrl+Down/Ctrl+Up or Cmd+Down/Cmd+Up
        if Settings.is_mac():
            type(Key.DOWN, modifier=KeyModifier.CMD)
        else:
            type(Key.DOWN, modifier=KeyModifier.CTRL)

        soap_wiki_footer_mark_initial = exists(soap_wiki_footer_pattern)
        assert_true(self, soap_wiki_footer_mark_initial, 'Successfully scrolled to footer by pressing Ctrl+Down '
                                                         'or Cmd+Down')

        if Settings.is_mac():
            type(Key.UP, modifier=KeyModifier.CMD)
        else:
            type(Key.UP, modifier=KeyModifier.CTRL)

        soap_wiki_header_mark_initial = exists(soap_wiki_header_mark_pattern)
        assert_true(self, soap_wiki_header_mark_initial, 'Successfully scrolled from footer to header by '
                                                         'pressing Ctrl+Up or Cmd+Up')
