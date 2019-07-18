# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bug 1325651 - Safe browsing is working in safe mode',
        test_case_id='215325',
        test_suite_id='69',
        locale=['en-US'],
        profile=Profiles.BRAND_NEW
    )
    def run(self, firefox):
        start_in_safe_mode_button_pattern = Pattern('start_in_safe_mode_button.png')
        about_support_title_pattern = Pattern('about_support_title.png')
        restart_button_pattern = Pattern('restart_button.png')

        navigate(LocalWeb.FIREFOX_TEST_SITE)

        test_site_opened = exists(LocalWeb.FIREFOX_IMAGE, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert test_site_opened, 'Firefox test site opened'

        next_tab()

        navigate(LocalWeb.POCKET_TEST_SITE)

        test_site_opened = exists(LocalWeb.POCKET_IMAGE, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert test_site_opened, 'Pocket test site opened'

        new_tab()

        navigate('about:support')

        about_support_page_opened = exists(about_support_title_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert about_support_page_opened, 'About Support page opened'

        about_support_title_loc = find(about_support_title_pattern)
        width, height = about_support_title_pattern.get_size()
        buttons_region = Region(about_support_title_loc.x, about_support_title_loc.y, width*2, height*5)

        copy_text_button_exists = exists('Copy raw data to clipboard', FirefoxSettings.FIREFOX_TIMEOUT,
                                         region=buttons_region)
        assert copy_text_button_exists, 'Copy raw data to clipboard button exists'

        click('Copy raw data to clipboard', region=buttons_region)

        time.sleep(FirefoxSettings.SHORT_FIREFOX_TIMEOUT)

        clipboard_before_restart = get_clipboard().partition('safeMode')

        restart_button_exists = exists('Restart with Add-ons Disabled', FirefoxSettings.FIREFOX_TIMEOUT)
        assert restart_button_exists, 'Restart with Add-ons Disabled button displayed'

        click('Restart with Add-ons Disabled')

        restart_button_displayed = exists(restart_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert restart_button_displayed, 'Restart button displayed'

        click(restart_button_pattern)

        start_in_safe_mode_button_displayed = exists(start_in_safe_mode_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert start_in_safe_mode_button_displayed, 'Start in safe mode button displayed'

        click(start_in_safe_mode_button_pattern)

        about_support_page_opened = exists(about_support_title_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert about_support_page_opened, 'About Support page opened'

        copy_text_button_exists = exists('Copy raw data to clipboard', FirefoxSettings.FIREFOX_TIMEOUT,
                                         region=buttons_region)
        assert copy_text_button_exists, 'Copy raw data to clipboard button exists'

        click('Copy raw data to clipboard', region=buttons_region)

        time.sleep(FirefoxSettings.SHORT_FIREFOX_TIMEOUT)

        clipboard_after_restart = get_clipboard().partition('safeMode')
        assert clipboard_after_restart[0] in clipboard_before_restart[0], 'about:support should have all information ' \
                                                                          'filled in'

        select_tab('1')

        test_site_opened = exists(LocalWeb.FIREFOX_IMAGE, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert test_site_opened, 'Firefox test site opened'

        select_tab('2')

        test_site_opened = exists(LocalWeb.POCKET_IMAGE, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert test_site_opened, 'Pocket test site opened'
