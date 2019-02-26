# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    test_details = pytest.mark.DETAILS(meta="Test experiment_root",
                                       description="Empty",
                                       fx_version="63",
                                       locale="en-US, zh-CN, es-ES, de, fr, ru, ar, ko, pt-PT, vi, pl, tr, ro, ja, zh-CN, es-ES, de",
                                       chanel="beta",
                                       test_case_id="1111", test_suite_id="888666", blocked_by="123333111")

    @test_details
    @pytest.mark.skip
    def test_run(self):
        # region = Region(0, 40, 200, 100)
        # region.highlight()
        # print(region.double_click(Pattern('test.png', application='firefox')))
        # print(region.exists('Project', 'Word found'))
        # result=region.exists('Search a very')

        # assert result==True ,"Assert_message for Image search test "
        assert 1 == 1, "Assert_message 2for experiment 2"
