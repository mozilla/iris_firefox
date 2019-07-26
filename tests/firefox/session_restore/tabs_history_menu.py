# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='All recently closed tabs can be reopened from the history menu',
        test_case_id='117178',
        test_suite_id='68',
        locales=Locales.ENGLISH,
    )
    def run(self, firefox):
        restore_tabs_pattern = Pattern('restore_all_tabs_button.png')
        recently_closed_pattern = Pattern('recently_closed_tabs.png')
        history_menu_bar_pattern = Pattern('history_menu_bar.png')
        tabs_list_pattern = Pattern('tabs_list.png')

        local_url = [LocalWeb.FIREFOX_TEST_SITE, LocalWeb.FIREFOX_TEST_SITE_2, LocalWeb.FOCUS_TEST_SITE,
                     LocalWeb.FOCUS_TEST_SITE_2, LocalWeb.MOZILLA_TEST_SITE, LocalWeb.POCKET_TEST_SITE]

        website_image_pattern = [LocalWeb.FIREFOX_LOGO, LocalWeb.FIREFOX_LOGO, LocalWeb.FOCUS_LOGO,
                                 LocalWeb.FOCUS_LOGO, LocalWeb.MOZILLA_LOGO, LocalWeb.POCKET_LOGO]

        for index in range(6):
            new_tab()
            navigate(local_url[index])
            website_loaded = exists(website_image_pattern[index], FirefoxSettings.SITE_LOAD_TIMEOUT)
            assert website_loaded, f'Website {index + 1} loaded'

        [close_tab() for _ in range(5)]

        one_tab_exists = exists(website_image_pattern[0], FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert one_tab_exists, 'One opened tab left. All 5 tabs were successfully closed.'

        # show menu bar
        key_down(Key.ALT)
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)  # time sleep for Linux
        key_up(Key.ALT)

        if OSHelper.is_mac():  # menu bar background may have transparency on MAC
            type(Key.F2, KeyModifier.CTRL)
            [type(Key.RIGHT) for tab_index in range(5)]
            type(Key.ENTER)
        else:
            history_menu_bar_exists = exists(history_menu_bar_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
            assert history_menu_bar_exists, 'History menu bar is visible.'
            click(history_menu_bar_pattern)

        recently_closed_menu = exists(recently_closed_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert recently_closed_menu, 'The History\'s button context menu is opened. Recently Closed Tabs is visible.'

        click(recently_closed_pattern)
        tabs_list_exists = exists(tabs_list_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert tabs_list_exists, 'Previously Opened Tabs list exists. A new menu ' \
                                 'is displayed containing the recently closed tabs'

        restore_tabs = exists(restore_tabs_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert restore_tabs, 'Restore tabs button available.'

        restore_tabs_location = find(restore_tabs_pattern)

        time.sleep(FirefoxSettings.SHORT_FIREFOX_TIMEOUT)

        click(restore_tabs_location, 0)

        #  check if all tabs reopened correctly
        tabs_count = len(website_image_pattern)
        for tab_index in range(6):
            if len(website_image_pattern) == 1:
                one_tab_left = exists(website_image_pattern[0], FirefoxSettings.SITE_LOAD_TIMEOUT)
                assert one_tab_left, f'All {tabs_count - 1} closed tabs are successfully reopened.'

            else:
                tab_exists = exists(website_image_pattern.pop(), FirefoxSettings.SITE_LOAD_TIMEOUT)
                assert tab_exists, f'Tab {tabs_count - tab_index} successfully reopened.'

                previous_tab()
