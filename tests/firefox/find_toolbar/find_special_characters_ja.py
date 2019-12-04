# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Search a word that contains special characters (2)",
        locale=["en-US"],
        test_case_id="127276",
        test_suite_id="2085",
        blocked_by={"id": "4283", "platform": [OSPlatform.LINUX, OSPlatform.WINDOWS]}
    )
    def run(self, firefox):
        first_japan_highlighted_pattern = Pattern("first_japan_highlighted.png")
        second_japan_highlighted_pattern = Pattern("second_japan_highlighted.png")
        japan_not_highlighted_pattern = Pattern("japan_not_highlighted.png")

        test_page_local = self.get_asset_path("ja.htm")
        navigate(test_page_local)

        page_loaded_anchor_exists = exists(LocalWeb.SOAP_WIKI_TEST_LABEL_PATTERN, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert page_loaded_anchor_exists, "The page is successfully loaded."

        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(FindToolbar.FINDBAR_TEXTBOX, FirefoxSettings.FIREFOX_TIMEOUT)
        assert find_toolbar_opened, "Find Toolbar is opened."

        paste("辻希美")

        selected_label_exists = exists(first_japan_highlighted_pattern)
        assert selected_label_exists, "The first one has a green background highlighted."

        not_selected_label_exists = exists(japan_not_highlighted_pattern)
        assert not_selected_label_exists, "The second one is not highlighted."

        find_next()

        second_highlighted_exists = exists(second_japan_highlighted_pattern)
        assert second_highlighted_exists, "The green box is moved with the current item."
