# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Scrolling with different settings at preferences-level.'
        self.test_case_id = '4713'
        self.test_suite_id = '102'
        self.locales = ['en-US']

    def run(self):
        checked_use_smooth_scrolling_pattern = Pattern('checked_use_smooth_scrolling.png')
        unchecked_use_smooth_scrolling_pattern = Pattern('unchecked_use_smooth_scrolling.png')
        history_paragraph_pattern = Pattern('history_paragraph.png')
        soap_wiki_header_pattern = Pattern('soap_wiki_header.png')

        if Settings.is_windows():
            scroll_height = SCREEN_HEIGHT*2
        elif Settings.is_linux():
            scroll_height = SCREEN_HEIGHT/100
        else:
            scroll_height = SCREEN_HEIGHT

        # Use smooth scrolling is disabled
        navigate('about:preferences#general')

        preferences_page_downloaded = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_NOT_SELECTED,
                                             DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, preferences_page_downloaded, 'The Preferences page is downloaded')

        paste('Use autoscrolling')

        checked_use_smooth_scrolling_exists = exists(checked_use_smooth_scrolling_pattern,
                                                               DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, checked_use_smooth_scrolling_exists, 'Use smooth scrolling option is displayed on the page')

        click(checked_use_smooth_scrolling_pattern)

        unchecked_use_smooth_scrolling_exists = exists(unchecked_use_smooth_scrolling_pattern,
                                                                 DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, unchecked_use_smooth_scrolling_exists, 'Use smooth scrolling option is disabled')

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_test_site_opened = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, 20)
        assert_true(self, soap_wiki_test_site_opened, 'The Soap Wiki test site is properly loaded')

        click(LocalWeb.SOAP_WIKI_SOAP_LABEL)

        # Scroll by mouse wheel
        scroll_by_mouse_wheel_to_footer = scroll_until_pattern_found(history_paragraph_pattern,
                                                                     scroll, (-scroll_height,))
        assert_true(self, scroll_by_mouse_wheel_to_footer, 'Successfully scrolled to footer by mouse scroll')

        scroll_by_mouse_wheel_to_header = scroll_until_pattern_found(soap_wiki_header_pattern,
                                                                     scroll, (scroll_height,))
        assert_true(self, scroll_by_mouse_wheel_to_header, 'Successfully scrolled to header by mouse scroll')

        # Scroll by pressing arrows
        scroll_by_arrows_to_footer = scroll_until_pattern_found(history_paragraph_pattern, repeat_key_down, (20,))
        assert_true(self, scroll_by_arrows_to_footer, 'Successfully scrolled to footer by pressing key down button')

        scroll_by_arrows_to_header = scroll_until_pattern_found(soap_wiki_header_pattern, repeat_key_up, (20,))
        assert_true(self, scroll_by_arrows_to_header, 'Successfully scrolled to header by pressing key up button')

        # Use smooth scrolling is disabled
        navigate('about:preferences#general')

        preferences_page_downloaded = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_NOT_SELECTED,
                                             DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, preferences_page_downloaded, 'The Preferences page is downloaded')

        paste('Use autoscrolling')

        unchecked_use_smooth_scrolling_exists = exists(unchecked_use_smooth_scrolling_pattern,
                                                                DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, unchecked_use_smooth_scrolling_exists, 'Use smooth scrolling option is enabled')

        click(unchecked_use_smooth_scrolling_pattern)

        checked_use_smooth_scrolling_exists = exists(checked_use_smooth_scrolling_pattern,
                                                              DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, checked_use_smooth_scrolling_exists, 'Use smooth scrolling option is displayed on the page')

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_test_site_opened_again = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, 20)
        assert_true(self, soap_wiki_test_site_opened_again, 'The Soap Wiki test site is properly loaded')

        click(LocalWeb.SOAP_WIKI_SOAP_LABEL)

        # Scroll by mouse wheel
        scroll_by_mouse_wheel_to_footer = scroll_until_pattern_found(history_paragraph_pattern,
                                                                     scroll, (-scroll_height,))
        assert_true(self, scroll_by_mouse_wheel_to_footer, 'Successfully scrolled to footer by mouse scroll')

        scroll_by_mouse_wheel_to_header = scroll_until_pattern_found(soap_wiki_header_pattern,
                                                                     scroll, (scroll_height,))
        assert_true(self, scroll_by_mouse_wheel_to_header, 'Successfully scrolled to header by mouse scroll')

        # Scroll by pressing arrows
        scroll_by_arrows_to_footer = scroll_until_pattern_found(history_paragraph_pattern, repeat_key_down, (20,))
        assert_true(self, scroll_by_arrows_to_footer, 'Successfully scrolled to footer by pressing key down button')

        scroll_by_arrows_to_header = scroll_until_pattern_found(soap_wiki_header_pattern, repeat_key_up, (20,))
        assert_true(self, scroll_by_arrows_to_header, 'Successfully scrolled to header by pressing key up button')
