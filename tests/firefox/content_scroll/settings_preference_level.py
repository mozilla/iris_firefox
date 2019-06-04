# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Scrolling with different settings at preferences-level.',
        test_case_id='4713',
        test_suite_id='102',
        locale=['en-US'],
    )
    def run(self, firefox):
        checked_use_smooth_scrolling_pattern = Pattern('checked_use_smooth_scrolling.png')
        unchecked_use_smooth_scrolling_pattern = Pattern('unchecked_use_smooth_scrolling.png')
        history_paragraph_pattern = Pattern('history_paragraph.png')
        soap_wiki_header_pattern = Pattern('soap_wiki_header.png')

        if OSHelper.is_windows():
            scroll_height = Screen.SCREEN_HEIGHT*2
        elif OSHelper.is_linux() or OSHelper.is_mac():
            scroll_height = Screen.SCREEN_HEIGHT/100

        # Use smooth scrolling is disabled
        navigate('about:preferences#general')

        preferences_page_downloaded = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_NOT_SELECTED,
                                             FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert preferences_page_downloaded is True, 'The Preferences page is downloaded'

        paste('Use autoscrolling')

        checked_use_smooth_scrolling_exists = exists(checked_use_smooth_scrolling_pattern,
                                                     FirefoxSettings.FIREFOX_TIMEOUT)
        assert checked_use_smooth_scrolling_exists is True, 'Use smooth scrolling option is displayed on the page'

        click(checked_use_smooth_scrolling_pattern)

        unchecked_use_smooth_scrolling_exists = exists(unchecked_use_smooth_scrolling_pattern,
                                                       FirefoxSettings.FIREFOX_TIMEOUT)
        assert unchecked_use_smooth_scrolling_exists is True, 'Use smooth scrolling option is disabled'

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_test_site_opened = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert soap_wiki_test_site_opened is True, 'The Soap Wiki test site is properly loaded'

        click(LocalWeb.SOAP_WIKI_SOAP_LABEL)

        # Scroll by mouse wheel
        scroll_by_mouse_wheel_to_footer = scroll_until_pattern_found(history_paragraph_pattern, Mouse().scroll,
                                                                     (None, -scroll_height), 20,
                                                                     FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
        assert scroll_by_mouse_wheel_to_footer is True, 'Successfully scrolled to footer by mouse scroll'

        scroll_by_mouse_wheel_to_header = scroll_until_pattern_found(soap_wiki_header_pattern, Mouse().scroll,
                                                                     (None, scroll_height), 20,
                                                                     FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
        assert scroll_by_mouse_wheel_to_header is True, 'Successfully scrolled to header by mouse scroll'

        # Scroll by pressing arrows
        scroll_by_arrows_to_footer = scroll_until_pattern_found(history_paragraph_pattern, repeat_key_down, (20,))
        assert scroll_by_arrows_to_footer is True, 'Successfully scrolled to footer by pressing key down button'

        scroll_by_arrows_to_header = scroll_until_pattern_found(soap_wiki_header_pattern, repeat_key_up, (20,))
        assert scroll_by_arrows_to_header is True, 'Successfully scrolled to header by pressing key up button'

        # Use smooth scrolling is disabled
        navigate('about:preferences#general')

        preferences_page_downloaded = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_NOT_SELECTED,
                                             FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert preferences_page_downloaded is True, 'The Preferences page is downloaded'

        paste('Use autoscrolling')

        unchecked_use_smooth_scrolling_exists = exists(unchecked_use_smooth_scrolling_pattern,
                                                       FirefoxSettings.FIREFOX_TIMEOUT)
        assert unchecked_use_smooth_scrolling_exists is True, 'Use smooth scrolling option is enabled'

        click(unchecked_use_smooth_scrolling_pattern)

        checked_use_smooth_scrolling_exists = exists(checked_use_smooth_scrolling_pattern,
                                                     FirefoxSettings.FIREFOX_TIMEOUT)
        assert checked_use_smooth_scrolling_exists is True, 'Use smooth scrolling option is displayed on the page'

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_test_site_opened_again = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert soap_wiki_test_site_opened_again is True, 'The Soap Wiki test site is properly loaded'

        click(LocalWeb.SOAP_WIKI_SOAP_LABEL)

        # Scroll by mouse wheel
        scroll_by_mouse_wheel_to_footer = scroll_until_pattern_found(history_paragraph_pattern, Mouse().scroll,
                                                                     (None, -scroll_height), 20,
                                                                     FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
        assert scroll_by_mouse_wheel_to_footer is True, 'Successfully scrolled to footer by mouse scroll'

        scroll_by_mouse_wheel_to_header = scroll_until_pattern_found(soap_wiki_header_pattern, Mouse().scroll,
                                                                     (None, scroll_height), 20,
                                                                     FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
        assert scroll_by_mouse_wheel_to_header is True, 'Successfully scrolled to header by mouse scroll'

        # Scroll by pressing arrows
        scroll_by_arrows_to_footer = scroll_until_pattern_found(history_paragraph_pattern, repeat_key_down, (20,))
        assert scroll_by_arrows_to_footer is True, 'Successfully scrolled to footer by pressing key down button'

        scroll_by_arrows_to_header = scroll_until_pattern_found(soap_wiki_header_pattern, repeat_key_up, (20,))
        assert scroll_by_arrows_to_header is True, 'Successfully scrolled to header by pressing key up button'
