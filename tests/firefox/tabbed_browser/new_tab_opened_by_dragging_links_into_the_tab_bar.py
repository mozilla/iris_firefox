# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="New Tabs can be opened by dragging the links into the tab bar",
        locale=["en-US"],
        test_case_id="134458",
        test_suite_id="2103",
    )
    def run(self, firefox):
        drag_hyperlink_pattern = Pattern('drag_hyperlink.png')
        drop_hyperlink_new_tab_pattern = Pattern('drop_hyperlink.png')
        tab_title_pattern = Pattern('tab_title.png')
        hyperlink_background_pattern = Pattern('hyperlink_background.png')
        current_page_url_pattern = Pattern('current_page_url.png')

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)
        drag_drop_hyperlink = exists(tab_title_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert drag_drop_hyperlink, 'The Web page could not load'

        hyperlink = exists(drag_hyperlink_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert hyperlink, 'Hyperlink does not exists'

        hyperlink_location = find(drag_hyperlink_pattern)
        hyperlink_width, hyperlink_height = drag_hyperlink_pattern.get_size()
        hyperlink_section_region = Region(
            hyperlink_location.x - hyperlink_width / 4,
            hyperlink_location.y - hyperlink_height / 2,
            hyperlink_width * 1.5,
            hyperlink_height * 2
        )
        
        hyperlink = exists(drag_hyperlink_pattern, FirefoxSettings.FIREFOX_TIMEOUT, hyperlink_section_region)
        assert hyperlink, 'Hyperlink does not exists in given region'

        # Drag a hyperlink and drop it in new tab bar
        drag_hyperlink_location = find(drag_hyperlink_pattern, hyperlink_section_region)
        drop_hyperlink_location = find(drop_hyperlink_new_tab_pattern)

        drag_drop(drag_hyperlink_location, drop_hyperlink_location,FirefoxSettings.FIREFOX_TIMEOUT,align='center')

        hyperlink_exists = exists(hyperlink_background_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert hyperlink_exists, "Could not open hyperlink in background"

        current_page_url = exists(current_page_url_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert current_page_url, "Current page url does not match with navigated url"
