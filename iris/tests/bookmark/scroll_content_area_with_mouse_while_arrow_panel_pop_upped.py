# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Open a bookmark in a New Tab from Bookmarks Sidebar'
        self.test_case_id = '175213'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        soap_scroll_content_pattern = Pattern('soap_scroll_content.png')
        site_information_panel_pattern = Pattern('site_information_panel.png')

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_label_exists = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, soap_wiki_label_exists, 'Soap page is opened')

        library_icon_exists = exists(NavBar.LIBRARY_MENU, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, library_icon_exists, 'The Library menu icon exists')

        click(NavBar.LIBRARY_MENU)

        bookmarks_menu_option_exists = exists(LibraryMenu.BOOKMARKS_OPTION, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, bookmarks_menu_option_exists, 'The Library menu is correctly displayed')

        mouse_move(LocalWeb.SOAP_WIKI_SOAP_LABEL)

        scroll_until_pattern_found(soap_scroll_content_pattern, scroll, (-SCREEN_HEIGHT, None), 100,
                                   Settings.TINY_FIREFOX_TIMEOUT/2)

        try:
            soap_wiki_label_not_exists = wait_vanish(LocalWeb.SOAP_WIKI_SOAP_LABEL.similar(.9),
                                                     Settings.SHORT_FIREFOX_TIMEOUT)
            assert_true(self, soap_wiki_label_not_exists,
                        'Scroll using mouse wheel is successful with library pop upped panel')
        except FindError:
            raise FindError('Content is still on the page')

        click(soap_scroll_content_pattern)

        page_home()

        hamburger_menu_icon_exists = exists(NavBar.HAMBURGER_MENU, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, hamburger_menu_icon_exists, 'Hamburger menu icon exists')

        click(NavBar.HAMBURGER_MENU)

        hamburger_menu_panel_exists = exists(HamburgerMenu.HAMBURGER_MENU_ZOOM_INDICATOR,
                                             Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, hamburger_menu_panel_exists, 'Hamburger menu panel is displayed')

        mouse_move(LocalWeb.SOAP_WIKI_SOAP_LABEL)

        scroll_until_pattern_found(soap_scroll_content_pattern, scroll, (-SCREEN_HEIGHT, None), 100,
                                   Settings.TINY_FIREFOX_TIMEOUT/2)

        try:
            soap_wiki_label_not_exists = wait_vanish(LocalWeb.SOAP_WIKI_SOAP_LABEL.similar(.9),
                                                     Settings.SHORT_FIREFOX_TIMEOUT)
            assert_true(self, soap_wiki_label_not_exists,
                        'Scroll using mouse wheel is successful with hamburger menu pop upped panel')
        except FindError:
            raise FindError('Content is still on the page')

        click(soap_scroll_content_pattern)

        page_home()

        site_information_icon_exists = exists(site_information_panel_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, site_information_icon_exists, 'Site information icon exists')

        click(site_information_panel_pattern)

        site_information_panel_exists = exists(SiteInformationPanel.SITE_INFORMATION_PANEL_LABEL,
                                               Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, site_information_panel_exists, 'Site information panel is displayed')

        mouse_move(LocalWeb.SOAP_WIKI_SOAP_LABEL)

        scroll_until_pattern_found(soap_scroll_content_pattern, scroll, (-SCREEN_HEIGHT, None), 100,
                                   Settings.TINY_FIREFOX_TIMEOUT / 2)

        try:
            soap_wiki_label_not_exists = wait_vanish(LocalWeb.SOAP_WIKI_SOAP_LABEL.similar(.9),
                                                     Settings.SHORT_FIREFOX_TIMEOUT)
            assert_true(self, soap_wiki_label_not_exists,
                        'Scroll using mouse wheel is successful with hamburger menu pop upped panel')
        except FindError:
            raise FindError('Content is still on the page')

        click(soap_scroll_content_pattern)

        page_home()

        star_button_exists = exists(LocationBar.STAR_BUTTON_UNSTARRED, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, star_button_exists, 'Star button icon exists')

        click(LocationBar.STAR_BUTTON_UNSTARRED)

        star_panel_exists = exists(Bookmarks.StarDialog.NEW_BOOKMARK, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, star_panel_exists, 'Star panel is displayed')

        mouse_move(LocalWeb.SOAP_WIKI_SOAP_LABEL)

        scroll_until_pattern_found(soap_scroll_content_pattern, scroll, (-SCREEN_HEIGHT, None), 100,
                                   Settings.TINY_FIREFOX_TIMEOUT / 2)

        try:
            soap_wiki_label_not_exists = wait_vanish(LocalWeb.SOAP_WIKI_SOAP_LABEL.similar(.9),
                                                     Settings.SHORT_FIREFOX_TIMEOUT)
            assert_true(self, soap_wiki_label_not_exists,
                        'Scroll using mouse wheel is successful with hamburger menu pop upped panel')
        except FindError:
            raise FindError('Content is still on the page')

        click(soap_scroll_content_pattern)

        page_home()
