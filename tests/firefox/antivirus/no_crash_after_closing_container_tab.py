# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='No crash or bluescreen after closing a container tab.',
        locale=['en-US'],
        test_case_id='219583',
        test_suite_id='3063'
    )
    def run(self, firefox):
        addons_logo_pattern = Pattern('addons_logo.png')
        add_addon_button_pattern = Pattern('add_addon_button.png')
        add_to_firefox_button_pattern = Pattern('add_to_firefox_button.png')
        find_addons_pattern = Pattern('find_addons.png')
        multi_account_logo_pattern = Pattern('multi_account_logo.png')
        ok_addon_button_pattern = Pattern('ok_addon_button.png')
        youtube_top_sites_logo_pattern = Pattern('youtube_top_sites_logo.png')
        twitter_top_sites_logo_pattern = Pattern('twitter_top_sites_logo.png')
        container_option_pattern = Pattern('container_option.png')
        personal_option_pattern = Pattern('personal_option.png')
        yotube_logo_pattern = Pattern('youtube_logo.png')
        twitter_logo_pattern = Pattern('twitter_favicon.png')
        personal_label_pattern = Pattern('personal_label.png')
        multi_account_logo_small_pattern = Pattern('multi_account_logo_small.png')

        navigate('https://addons.mozilla.org/en-US/firefox/')

        addons_page_opened = exists(addons_logo_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert addons_page_opened, 'Firefox Add-ons page opened'

        find_addons_field_displayed = exists(find_addons_pattern)
        assert find_addons_field_displayed, 'Find add-ons field displayed'

        click(find_addons_pattern)

        type('Multi-account', interval=0.5)

        multi_account_suggest = exists(multi_account_logo_small_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert multi_account_suggest, 'Multi-account add-on displayed in suggestions'

        type(Key.DOWN)
        type(Key.ENTER)

        multi_account_page_opened = exists(multi_account_logo_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert multi_account_page_opened, 'Firefox Multi-Account Containers page opened'

        add_to_firefox_button_displayed = exists(add_to_firefox_button_pattern)
        assert add_to_firefox_button_displayed, 'Add to Firefox button displayed'

        click(add_to_firefox_button_pattern)

        add_addon_popup_displayed = exists(add_addon_button_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert add_addon_popup_displayed, 'Add Firefox Multi-Account Containers? pop-up displayed'

        click(add_addon_button_pattern)

        addon_has_been_added = exists(ok_addon_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert addon_has_been_added, 'Firefox Multi-Account Containers has been added to Firefox'

        click(ok_addon_button_pattern)

        navigate('about:newtab')

        youtube_top_sites_logo_exists = exists(youtube_top_sites_logo_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert youtube_top_sites_logo_exists, 'Youtube top sites logo exists'

        right_click(youtube_top_sites_logo_pattern)

        youtube_container_option_exists = exists(container_option_pattern)
        assert youtube_container_option_exists, 'Container option exists'

        click(container_option_pattern)

        youtube_personal_option_exists = exists(personal_option_pattern)
        assert youtube_personal_option_exists, 'Container option exists'

        click(personal_option_pattern)

        twitter_top_sites_logo_exists = exists(twitter_top_sites_logo_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert twitter_top_sites_logo_exists, 'Twitter top sites logo exists'

        right_click(twitter_top_sites_logo_pattern)

        twitter_container_option_exists = exists(container_option_pattern)
        assert twitter_container_option_exists, 'Container option exists'

        click(container_option_pattern)

        twitter_personal_option_exists = exists(personal_option_pattern)
        assert twitter_personal_option_exists, 'Container option exists'

        click(personal_option_pattern)

        select_tab(2)

        youtube_opened = exists(yotube_logo_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert youtube_opened, 'Youtube site is successfully loaded'

        youtube_opened_in_container_tab = exists(personal_label_pattern)
        assert youtube_opened_in_container_tab, 'Youtube site is opened in container tab'

        select_tab(3)

        twitter_opened = exists(twitter_logo_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert twitter_opened, 'Twitter site is successfully loaded'

        twitter_opened_in_container_tab = exists(personal_label_pattern)
        assert twitter_opened_in_container_tab, 'Twitter site is opened in container tab'

        close_tab()

        try:
            twitter_tab_closed = wait_vanish(twitter_logo_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            assert twitter_tab_closed, 'The container tab is closed.'
        except FindError:
            raise FindError('The container tab is not closed.')

        reload_page()

        no_crashes_occurred = exists(yotube_logo_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert no_crashes_occurred, 'No crash or blue screen after closing a container tab.'
