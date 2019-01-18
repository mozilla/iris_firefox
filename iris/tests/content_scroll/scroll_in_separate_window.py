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
        iris_tab_logo_pattern = Pattern('iris_logo_tab.png')

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

        # Scrolling test in the initial window
        # Scroll by mouse wheel
        for times_scroll_down in range(100):
            scroll(-mouse_wheel_steps)
            soap_wiki_footer_mark = exists(soap_wiki_footer_pattern)
            if soap_wiki_footer_mark:
                assert_true(self, soap_wiki_footer_mark, "New window: Successfully scrolled to footer by mouse scroll")
                break

        for times_scroll_up in range(100):
            scroll(mouse_wheel_steps)
            soap_wiki_header_mark = exists(soap_wiki_header_mark_pattern)
            if soap_wiki_header_mark:
                assert_true(self, soap_wiki_header_mark, "New window: Successfully scrolled from footer to "
                                                         "header by mouse scroll")
                break

        # Scroll by pressing arrows
        for times_arrow_press in range(100):
            repeat_key_down(30)
            soap_wiki_footer_mark = exists(soap_wiki_footer_pattern)
            if soap_wiki_footer_mark:
                assert_true(self, soap_wiki_footer_mark, "New window: Successfully scrolled to footer by pressing "
                                                         "arrows")
                break

        for times_arrow_press in range(100):
            repeat_key_up(30)
            soap_wiki_header_mark = exists(soap_wiki_header_mark_pattern)
            if soap_wiki_header_mark:
                assert_true(self, soap_wiki_header_mark, "New window: Successfully scrolled from footer to header "
                                                         "by pressing arrows")
                break

        # Scroll by pressing Page Up/Page Down
        for times_page_down_press in range(10):
            page_down()
            soap_wiki_footer_mark = exists(soap_wiki_footer_pattern)
            if soap_wiki_footer_mark:
                assert_true(self, soap_wiki_footer_mark, "New window: Successfully scrolled to footer by pressing "
                                                         "Page Down")
                break

        for times_page_up_press in range(10):
            page_up()
            soap_wiki_header_mark = exists(soap_wiki_header_mark_pattern)
            if soap_wiki_header_mark:
                assert_true(self, soap_wiki_header_mark, "New window: Successfully scrolled from footer to header "
                                                         "by pressing Page Up")
                break

        # Scroll by pressing Space
        for times_space_press in range(10):
            type(Key.SPACE)
            soap_wiki_footer_mark = exists(soap_wiki_footer_pattern)
            if soap_wiki_footer_mark:
                assert_true(self, soap_wiki_footer_mark, "New window: Successfully scrolled to footer by pressing "
                                                         "Space")
                page_home()
                break

        # Scroll by pressing Ctrl+Down/Ctrl+Up or Cmd+Down/Cmd+Up
        if Settings.is_mac():
            type(Key.DOWN, modifier=KeyModifier.CMD)
        if Settings.is_windows():
            type(Key.DOWN, modifier=KeyModifier.CTRL)

        soap_wiki_footer_mark = exists(soap_wiki_footer_pattern)
        assert_true(self, soap_wiki_footer_mark, "New window: Successfully scrolled to footer by pressing "
                                                 "Ctrl+Down or Cmd+Down")

        if Settings.is_mac():
            type(Key.UP, modifier=KeyModifier.CMD)
        if Settings.is_windows():
            type(Key.UP, modifier=KeyModifier.CTRL)

        soap_wiki_header_mark = exists(soap_wiki_header_mark_pattern)
        assert_true(self, soap_wiki_header_mark, "New window: Successfully scrolled from footer to header by "
                                                 "pressing Ctrl+Up or Cmd+Up")

        # Move the tab back into initial window
        soap_wiki_new_window_tab_location = find(soap_wiki_tab_pattern)
        location_for_new_window_drag = Location.right(soap_wiki_new_window_tab_location, away_x=500)

        double_click(location_for_new_window_drag)

        soap_wiki_tab_pattern_to_move = find(soap_wiki_tab_pattern)
        location_to_hover = Location.right(soap_wiki_tab_pattern_to_move, away_x=1200)

        drag_drop(soap_wiki_tab_pattern, location_to_hover)

        soap_wiki_test_site_moved_to_initial = exists(soap_wiki_tab_pattern, 20)
        iris_tab_displayed = exists(iris_tab_logo_pattern, 20)
        assert_true(self, soap_wiki_test_site_moved_to_initial and iris_tab_displayed, 'The Soap Wiki test site '
                                                                                       'successfully moved back')
        click(LocalWeb.SOAP_WIKI_SOAP_LABEL)

        # Scrolling test in the initial window
        # Scroll by mouse wheel
        for times_scroll_down in range(100):
            scroll(-mouse_wheel_steps)
            soap_wiki_footer_mark = exists(soap_wiki_footer_pattern)
            if soap_wiki_footer_mark:
                assert_true(self, soap_wiki_footer_mark, "Initial window: Successfully scrolled to footer by mouse "
                                                         "scroll")
                break

        for times_scroll_up in range(100):
            scroll(mouse_wheel_steps)
            soap_wiki_header_mark = exists(soap_wiki_header_mark_pattern)
            if soap_wiki_header_mark:
                assert_true(self, soap_wiki_header_mark, "Initial window: Successfully scrolled from footer to "
                                                         "header by mouse scroll")
                break

        # Scroll by pressing arrows
        for times_arrow_press in range(100):
            repeat_key_down(30)
            soap_wiki_footer_mark = exists(soap_wiki_footer_pattern)
            if soap_wiki_footer_mark:
                assert_true(self, soap_wiki_footer_mark, "Initial window: Successfully scrolled to footer by pressing "
                                                         "arrows")
                break

        for times_arrow_press in range(100):
            repeat_key_up(30)
            soap_wiki_header_mark = exists(soap_wiki_header_mark_pattern)
            if soap_wiki_header_mark:
                assert_true(self, soap_wiki_header_mark, "Initial window: Successfully scrolled from footer to header "
                                                         "by pressing arrows")
                break

        # Scroll by pressing Page Up/Page Down
        for times_page_down_press in range(10):
            page_down()
            soap_wiki_footer_mark = exists(soap_wiki_footer_pattern)
            if soap_wiki_footer_mark:
                assert_true(self, soap_wiki_footer_mark, "Initial window: Successfully scrolled to footer by pressing "
                                                         "Page Down")
                break

        for times_page_up_press in range(10):
            page_up()
            soap_wiki_header_mark = exists(soap_wiki_header_mark_pattern)
            if soap_wiki_header_mark:
                assert_true(self, soap_wiki_header_mark, "Initial window: Successfully scrolled from footer to header "
                                                         "by pressing Page Up")
                break

        # Scroll by pressing Space
        for times_space_press in range(10):
            type(Key.SPACE)
            soap_wiki_footer_mark = exists(soap_wiki_footer_pattern)
            if soap_wiki_footer_mark:
                assert_true(self, soap_wiki_footer_mark, "Initial window: Successfully scrolled to footer by pressing "
                                                         "Space")
                page_home()
                break

        # Scroll by pressing Ctrl+Down/Ctrl+Up or Cmd+Down/Cmd+Up
        if Settings.is_mac():
            type(Key.DOWN, modifier=KeyModifier.CMD)
        if Settings.is_windows():
            type(Key.DOWN, modifier=KeyModifier.CTRL)

        soap_wiki_footer_mark = exists(soap_wiki_footer_pattern)
        assert_true(self, soap_wiki_footer_mark, "Initial window: Successfully scrolled to footer by pressing "
                                                 "Ctrl+Down or Cmd+Down")

        if Settings.is_mac():
            type(Key.UP, modifier=KeyModifier.CMD)
        if Settings.is_windows():
            type(Key.UP, modifier=KeyModifier.CTRL)

        soap_wiki_header_mark = exists(soap_wiki_header_mark_pattern)
        assert_true(self, soap_wiki_header_mark, "Initial window: Successfully scrolled from footer to header by "
                                                 "pressing Ctrl+Up or Cmd+Up")



