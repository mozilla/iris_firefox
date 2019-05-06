# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


def open_test_case_assets_folder_in_file_manager():
    path_to_test_assets = PathManager.get_current_test_asset_dir('')

    if OSHelper.is_linux():
        type(text='l', modifier=KeyModifier.CTRL)
        paste(path_to_test_assets)
        type(Key.ENTER)
    elif OSHelper.is_mac():
        type(text='g', modifier=[KeyModifier.SHIFT, KeyModifier.CMD])
        paste(path_to_test_assets)
        type(Key.ENTER)
    elif OSHelper.is_windows():
        type(text='l', modifier=KeyModifier.CTRL)
        paste(path_to_test_assets)
        type(Key.ENTER)


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Firefox Regular Usage.',
        locale=[Locales.ENGLISH],
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
        assert exists(load_temporary_addon_button_pattern, Settings.DEFAULT_SYSTEM_DELAY), \
            'Debugging page is successfully loaded and contains \'Load temporary addon\' button.'

        click(load_temporary_addon_button_pattern)
        assert exists(popup_open_button_pattern, Settings.DEFAULT_SYSTEM_DELAY), \
            '\'Load temporary add-on\' popup is opened.'

        open_test_case_assets_folder_in_file_manager()
        assert exists(theme_file_icon_pattern, Settings.DEFAULT_UI_DELAY), 'Theme file is available.'

        click(theme_file_icon_pattern)
        type(Key.ENTER)
        assert exists(home_icon_with_applied_theme_pattern, Settings.DEFAULT_SYSTEM_DELAY), \
            'Theme successfully applied.'

        click(load_temporary_addon_button_pattern)
        assert exists(popup_open_button_pattern, Settings.DEFAULT_SYSTEM_DELAY), \
            '\'Load temporary add-on\' popup is opened.'
        assert exists(addon_file_icon_pattern, Settings.DEFAULT_SYSTEM_DELAY), 'Addon file is available.'

        click(addon_file_icon_pattern)
        type(Key.ENTER)
        assert exists(adblock_icon_pattern, Settings.DEFAULT_SYSTEM_DELAY), 'Addon successfully installed.'

        click(home_icon_with_applied_theme_pattern)
        assert exists(new_tab_highlighted_with_theme_applied_pattern, Settings.DEFAULT_SYSTEM_DELAY), \
            'The \'about:newtab\' page is opened.'

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)
        assert exists(soap_wiki_page_article_header_pattern, Settings.DEFAULT_SITE_LOAD_TIMEOUT), \
            'The website is loaded without any issue.'
        close_window()
