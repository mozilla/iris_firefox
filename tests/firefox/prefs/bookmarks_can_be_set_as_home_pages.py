# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bookmarks can be set as home pages ',
        locale=['en-US'],
        test_case_id='2241',
        test_suite_id='161468'
    )
    def run(self, firefox):
        homepage_preferences_pattern = Pattern('homepage_preferences.png')
        default_setting_home_pattern = Pattern('default_new_tab_setting_home.png')
        custom_url_option_pattern = Pattern('custom_url_option.png')
        use_current_page_option_pattern = Pattern('use_current_page_option.png')
        use_bookmark_option_pattern = Pattern('use_bookmark_option.png')
        url_field_pattern = Pattern('url_field.png')
        getting_started_bookmark_pattern = Pattern('getting_started_bookmark.png')
        bookmarks_toolbar_folder_pattern = Pattern('bookmarks_toolbar_prefs.png')
        getting_started_tab_pattern = Pattern('get_started_tab.png')

        navigate('about:preferences#home')

        preferences_page_opened = exists(homepage_preferences_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert preferences_page_opened, 'The about:preferences page is successfully loaded.'

        homepage_preferences_location = find(homepage_preferences_pattern)
        homepage_preferences_width, homepage_preferences_height = homepage_preferences_pattern.get_size()
        homepage_section_region = Region(homepage_preferences_location.x, homepage_preferences_location.y,
                                         homepage_preferences_width*3, int(homepage_preferences_height*1.5))

        home_option_displayed = exists(default_setting_home_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                                       homepage_section_region)
        assert home_option_displayed, 'The options for "Home" section are displayed.'

        click(default_setting_home_pattern, region=homepage_section_region)

        custom_option_displayed = exists(custom_url_option_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert custom_option_displayed, 'The \'Custom\' option for "Home" section is displayed.'

        click(custom_url_option_pattern)

        bookmark_option_displayed = exists(url_field_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmark_option_displayed, 'The \'Paste a URL... \' field is displayed.'

        url_field_location = find(url_field_pattern)

        bookmark_option_displayed = exists(use_bookmark_option_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmark_option_displayed, 'The \'Use bookmark...\' button is displayed.'

        custom_option_displayed = exists(use_current_page_option_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert custom_option_displayed, 'The \'Use current pages\' button is displayed.'

        click(use_bookmark_option_pattern)

        bookmarks_toolbar_folder_exists = exists(bookmarks_toolbar_folder_pattern,
                                                 FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmarks_toolbar_folder_exists, 'Bookmarks toolbar folder displayed'

        double_click(bookmarks_toolbar_folder_pattern)

        getting_started_bookmark_displayed = exists(getting_started_bookmark_pattern,
                                                    FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert getting_started_bookmark_displayed, "Thr Getting Started bookmark displayed"

        double_click(getting_started_bookmark_pattern)

        time.sleep(Settings.DEFAULT_UI_DELAY)

        click(url_field_location)

        edit_select_all()
        copy_to_clipboard()

        time.sleep(Settings.DEFAULT_UI_DELAY)

        field_populated = get_clipboard()
        assert 'https://www.mozilla.org/en-US/firefox/central/' in field_populated, \
            'The field is populated with the bookmark]\'s link'

        quit_firefox()

        firefox.start(url='', image=NavBar.HOME_BUTTON)

        home_page_displayed = exists(getting_started_tab_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert home_page_displayed, 'The selected bookmark is set as homepage.'
