# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Firefox Regular Usage',
        locale=['en-US'],
        test_case_id='217855',
        test_suite_id='3063'
    )
    def run(self, firefox):
        soap_wiki_page_article_header_pattern = Pattern('wiki_article_header.png')
        new_tab_highlighted_with_theme_applied_pattern = Pattern('new_tab_highlighted_theme_applied.png')
        adblock_icon_pattern = Pattern('adblock_icon.png')
        addon_file_icon_pattern = Pattern('addon_file_icon.png')
        home_icon_with_applied_theme_pattern = Pattern('home_icon_theme_applied.png')
        theme_file_icon_pattern = Pattern('theme_file_icon.png')
        popup_open_button_pattern = Pattern('popup_open_button.png')
        load_temporary_addon_button_pattern = Pattern('load_temporary_addon_button.png')

        navigate('about:debugging')

        debugging_page_loaded = exists(load_temporary_addon_button_pattern, Settings.FIREFOX_TIMEOUT)
        assert debugging_page_loaded is True,\
            'Debugging page is successfully loaded and contains \'Load temporary addon\' button.'

        click(load_temporary_addon_button_pattern)

        popup_opened = exists(popup_open_button_pattern, Settings.FIREFOX_TIMEOUT)
        assert popup_opened is True, '\'Load temporary add-on\' popup is opened'

        assets_path = self.get_asset_path('')

        select_folder_location_bar()

        paste(assets_path)
        time.sleep(Settings.DEFAULT_UI_DELAY)
        type(Key.ENTER)

        theme_file_is_available = exists(theme_file_icon_pattern, FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        assert theme_file_is_available is True, 'Theme file is available.'

        click(theme_file_icon_pattern, 1)
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        type(Key.ENTER)

        theme_applied = exists(home_icon_with_applied_theme_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert theme_applied is True, 'Theme successfully applied.'

        click(load_temporary_addon_button_pattern)

        popup_opened = exists(popup_open_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert popup_opened is True, '\'Load temporary add-on\' popup is opened.'

        addon_file_is_available = exists(addon_file_icon_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert addon_file_is_available is True, 'Addon file is available.'

        click(addon_file_icon_pattern, 1)
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        type(Key.ENTER)

        addon_installed = exists(adblock_icon_pattern, FirefoxSettings.FIREFOX_TIMEOUT) \
            or exists('theme.images.theme_frame')
        assert addon_installed is True, 'Addon successfully installed.'

        click(home_icon_with_applied_theme_pattern)

        new_tab_opened = exists(new_tab_highlighted_with_theme_applied_pattern.similar(0.6),
                                FirefoxSettings.FIREFOX_TIMEOUT)
        assert new_tab_opened is True, 'The \'about:newtab\' page is opened.'

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        page_loaded = exists(soap_wiki_page_article_header_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert page_loaded is True, 'The website is loaded without any issue.'
