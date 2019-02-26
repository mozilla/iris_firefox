# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    test_details = pytest.mark.DETAILS(meta="Awesomebar_child_test2",
                                       description="test_child2",
                                       fx_version="63",
                                       locale="en-US, zh-CN, es-ES, de, fr, ru, ar, ko, pt-PT, vi, pl, tr, ro, ja, zh-CN, es-ES, de",
                                       chanel="beta",
                                       test_case_id="1111", test_suite_id="666", blocked_by="232111")

    @test_details
    def test_run(self):
        assert 1 == 1, "Assert_message 1for experiment 2"
        assert 1 == 1, "Assert_message 2for experiment 2"
