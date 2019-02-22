# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *



class Test(FirefoxTest):
    name = "Test experiment"
    description = "This test is just an experiment."
    fx_version = "63"
    locale = "en-US, zh-CN, es-ES, de"
    chanel = "beta"
    test_case_id = "435344"
    test_suite_id = "345444"
    blocked_by = ""


    @pytest.mark.skip
    def test_run(self):
        # region = Region(0, 40, 200, 100)
        # region.highlight()
        # print(region.double_click(Pattern('test.png', application='firefox')))
        # print(region.exists('Project', 'Word found'))
        # result=region.exists('Search a very')

        # assert result==True ,"Assert_message for Image search test "
        assert 1 == 1, "Assert_message 2for experiment 2"


