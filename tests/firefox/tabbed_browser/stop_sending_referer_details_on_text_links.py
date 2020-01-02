# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Stop sending referer details on text links",
        locale=["en-US"],
        test_case_id="139614",
        test_suite_id="2103",
    )
    def run(self, firefox):
        raw_paste_data_pattern = Pattern("raw_paste_data.png")
        what_is_my_referer_link_pattern = Pattern("whatismyreferer_link.png")
        what_is_my_referer_link_selected_pattern = Pattern("whatismyreferer_link_selected.png")
        your_http_referer_pattern = Pattern("your_http_referer.png")
        no_referer_hidden_pattern = Pattern("no_referer_hidden.png")

        navigate("https://pastebin.com/QD6QHKn3")

        raw_paste_data_expected = exists(raw_paste_data_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert raw_paste_data_expected, "'RAW paste data' section does not exist in 'pastebin.com'"

        raw_paste_data_location = find(raw_paste_data_pattern)
        raw_paste_data_region = Region(raw_paste_data_location.x,
                                       raw_paste_data_location.y,
                                       Screen.SCREEN_WIDTH / 2,
                                       Screen.SCREEN_HEIGHT / 5)
        what_is_my_referer_link_expected = exists(what_is_my_referer_link_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                                                  raw_paste_data_region)
        assert what_is_my_referer_link_expected, \
            "'https://www.whatismyreferer.com/' link not found in RAW paste data text area "

        click(what_is_my_referer_link_pattern)
        type("a", KeyModifier.CTRL)

        selected_link_expected = exists(what_is_my_referer_link_selected_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert selected_link_expected, "'https://www.whatismyreferer.com/' link not selected"

        right_click(what_is_my_referer_link_selected_pattern, region=raw_paste_data_region)
        time.sleep(Settings.DEFAULT_UI_DELAY_SHORT)
        if OSHelper.is_windows():
            type("t", KeyModifier.SHIFT)
        else:
            type("t", KeyModifier.CTRL)
        type(Key.ENTER)

        next_tab()

        your_http_referer_pattern_expected = exists(your_http_referer_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert your_http_referer_pattern_expected, "'Your HTTP referer' section does not exist in 'whatismyreferer.com'"

        your_http_referer_location = find(your_http_referer_pattern)
        your_http_referer_region = Region(your_http_referer_location.x,
                                          your_http_referer_location.y,
                                          Screen.SCREEN_WIDTH / 2,
                                          Screen.SCREEN_HEIGHT / 5)
        no_referer_hidden_expected = exists(no_referer_hidden_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                                            your_http_referer_region)
        assert no_referer_hidden_expected, "'No referer / hidden' not found under the 'Your HTTP referer' section"
