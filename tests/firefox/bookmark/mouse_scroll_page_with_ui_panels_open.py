# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bug 1471415 - No longer able to scroll content area with mouse wheel while arrow panel pop-upped',
        locale=['en-US'],
        test_case_id='175213',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        soap_scroll_content_pattern = Pattern('soap_scroll_content.png')
        site_information_panel_pattern = Pattern('site_information_panel.png')

        if OSHelper.is_windows():
            scroll_value = Screen.SCREEN_HEIGHT
        elif OSHelper.is_linux():
            scroll_value = Screen.SCREEN_HEIGHT/100
        else:
            scroll_value = Screen.SCREEN_HEIGHT/20

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_label_exists = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert soap_wiki_label_exists is True, 'Soap page is opened'

        library_icon_exists = exists(NavBar.LIBRARY_MENU, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert library_icon_exists is True, 'The Library menu icon exists'

        click(NavBar.LIBRARY_MENU)

        bookmarks_menu_option_exists = exists(LibraryMenu.BOOKMARKS_OPTION, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmarks_menu_option_exists is True, 'The Library menu is correctly displayed'

        hover(LocalWeb.SOAP_WIKI_SOAP_LABEL)

        scroll_until_pattern_found(soap_scroll_content_pattern, Mouse().scroll, (None, -scroll_value), 100,
                                   FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)

        try:
            soap_wiki_label_not_exists = wait_vanish(LocalWeb.SOAP_WIKI_SOAP_LABEL.similar(.9),
                                                     FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
            assert soap_wiki_label_not_exists is True, 'Scroll using mouse wheel is successful with ' \
                                                       'library pop upped panel'
        except FindError:
            raise FindError('Content is still on the page')

        click(soap_scroll_content_pattern)

        if not OSHelper.is_mac():
            page_home()
        else:
            type(text=Key.UP, modifier=KeyModifier.CMD)

        hamburger_menu_icon_exists = exists(NavBar.HAMBURGER_MENU, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert hamburger_menu_icon_exists  is True, 'Hamburger menu icon exists'

        click(NavBar.HAMBURGER_MENU)

        hamburger_menu_panel_exists = exists(HamburgerMenu.HAMBURGER_MENU_ZOOM_INDICATOR,
                                             FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert hamburger_menu_panel_exists is True, 'Hamburger menu panel is displayed'

        hover(LocalWeb.SOAP_WIKI_SOAP_LABEL.similar(.7))

        scroll_until_pattern_found(soap_scroll_content_pattern, Mouse().scroll, (None, -scroll_value), 100,
                                   FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)

        try:
            soap_wiki_label_not_exists = wait_vanish(LocalWeb.SOAP_WIKI_SOAP_LABEL.similar(.9),
                                                     FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
            assert soap_wiki_label_not_exists is True, 'Scroll using mouse wheel is successful with ' \
                                                       'hamburger menu pop upped panel'
        except FindError:
            raise FindError('Content is still on the page')

        click(soap_scroll_content_pattern)

        if not OSHelper.is_mac():
            page_home()
        else:
            type(text=Key.UP, modifier=KeyModifier.CMD)

        site_information_icon_exists = exists(site_information_panel_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert site_information_icon_exists is True, 'Site information icon exists'

        click(site_information_panel_pattern)

        site_information_panel_exists = exists(site_information_panel_pattern,
                                               FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert site_information_panel_exists is True, 'Site information panel is displayed'

        hover(LocalWeb.SOAP_WIKI_SOAP_LABEL.similar(.7))

        scroll_until_pattern_found(soap_scroll_content_pattern, Mouse().scroll, (None, -scroll_value), 100,
                                   FirefoxSettings.TINY_FIREFOX_TIMEOUT / 2)

        try:
            soap_wiki_label_not_exists = wait_vanish(LocalWeb.SOAP_WIKI_SOAP_LABEL.similar(.9),
                                                     FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
            assert soap_wiki_label_not_exists is True, 'Scroll using mouse wheel is successful with ' \
                                                       'hamburger menu pop upped panel'
        except FindError:
            raise FindError('Content is still on the page')

        click(soap_scroll_content_pattern)

        if not OSHelper.is_mac():
            page_home()
        else:
            type(text=Key.UP, modifier=KeyModifier.CMD)

        star_button_exists = exists(LocationBar.STAR_BUTTON_UNSTARRED, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert star_button_exists is True, 'Star button icon exists'

        click(LocationBar.STAR_BUTTON_UNSTARRED)

        star_panel_exists = exists(Bookmarks.StarDialog.NEW_BOOKMARK, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert star_panel_exists is True, 'Star panel is displayed'

        hover(LocalWeb.SOAP_WIKI_SOAP_LABEL.similar(.7))

        scroll_until_pattern_found(soap_scroll_content_pattern, Mouse().scroll, (None, -scroll_value), 100,
                                   FirefoxSettings.TINY_FIREFOX_TIMEOUT / 2)

        try:
            soap_wiki_label_not_exists = wait_vanish(LocalWeb.SOAP_WIKI_SOAP_LABEL.similar(.9),
                                                     FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
            assert soap_wiki_label_not_exists is True, 'Scroll using mouse wheel is successful with star ' \
                                                       'panel pop upped panel'
        except FindError:
            raise FindError('Content is still on the page')

        click(soap_scroll_content_pattern)

        if not OSHelper.is_mac():
            page_home()
        else:
            type(text=Key.UP, modifier=KeyModifier.CMD)
