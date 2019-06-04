# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description="Scrolling works properly on popular websites. ",
        test_case_id="C4664",
        test_suite_id="102",
        locale=["en-US"],
    )
    def run(self, firefox):
        soap_wiki_footer_pattern = Pattern('soap_wiki_footer.png')
        soap_wiki_header_mark_pattern = Pattern('soap_wiki_header.png')

        mouse_wheel_steps = 200
        if OSHelper.is_windows():
            mouse_wheel_steps = 1600

        new_tab()
        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_test_site_opened = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, 20)
        assert soap_wiki_test_site_opened is True, 'The Soap Wiki test site is properly loaded'

        click(LocalWeb.SOAP_WIKI_SOAP_LABEL)

        # Scroll by mouse wheel
        scroll_by_mouse_wheel_to_footer = scroll_until_pattern_found(soap_wiki_footer_pattern,
                                                                     Mouse().scroll, (0, -mouse_wheel_steps,))
        assert scroll_by_mouse_wheel_to_footer is True, 'Successfully scrolled to footer by mouse scroll'

        scroll_by_mouse_wheel_to_header = scroll_until_pattern_found(soap_wiki_header_mark_pattern,
                                                                     Mouse().scroll, (0, mouse_wheel_steps,))
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
        assert soap_wiki_header_mark is True, 'Successfully scrolled from footer to ' \
                                              'header by pressing Ctrl+Up or Cmd+Up'
