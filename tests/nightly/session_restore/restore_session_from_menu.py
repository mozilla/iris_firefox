# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.nightly.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Previous Session can be restored from the Firefox menu",
        test_case_id="114837",
        test_suite_id="68",
        locales=Locales.ENGLISH,
        blocked_by={"id": "issue_4118", "platform": OSPlatform.LINUX},
    )
    def run(self, firefox):
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        test_site_opened = exists(
            LocalWeb.MOZILLA_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT
        )
        assert test_site_opened, "Mozilla test website is opened"

        new_tab()

        navigate(LocalWeb.POCKET_TEST_SITE)

        test_site_opened = exists(
            LocalWeb.POCKET_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT
        )
        assert test_site_opened, "Pocket test website is opened"

        if OSHelper.is_windows():
            minimize_window()
            firefox.restart()
            maximize_window()
        else:
            firefox.restart()

        firefox_restarted = exists(
            LocalWeb.IRIS_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT
        )
        assert firefox_restarted, "Firefox restarted successfully"

        if OSHelper.is_linux():
            DELAY = 0.5
            restore_firefox_focus()
            select_location_bar()
            type(Key.TAB)
            time.sleep(DELAY)
            type(Key.TAB)
            time.sleep(DELAY)
            type(Key.RIGHT)
            time.sleep(DELAY)
            type(Key.RIGHT)
            time.sleep(DELAY)
            type(Key.RIGHT)
            time.sleep(DELAY)
            type(Key.ENTER)
            time.sleep(DELAY)
            try:
                region = Screen.RIGHT_HALF
                region.click("Restore")
            except FindError:
                raise FindError("Failed to click the Restore option.")
        else:
            click_hamburger_menu_option("Restore")

        time.sleep(Settings.DEFAULT_SYSTEM_DELAY)
        next_tab()

        first_tab_restored = exists(
            LocalWeb.MOZILLA_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT
        )
        assert first_tab_restored, "Mozilla test website is restored"

        next_tab()

        second_tab_restored = exists(
            LocalWeb.POCKET_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT
        )
        assert second_tab_restored, "Pocket test website is restored"

        all_tab_restored = first_tab_restored and second_tab_restored
        assert (
            all_tab_restored
        ), "The previous session is successfully restored (All previously closed tabs are successfully restored)."
