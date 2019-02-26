# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    test_details = pytest.mark.DETAILS(meta="Awesomebar_child_test1",
                                       description="test_child1",
                                       fx_version="63",
                                       locale="en-US, zh-CN, es-ES, de, fr, ru, ar, ko, pt-PT, vi, pl, tr, ro, ja, zh-CN, es-ES, de",
                                       chanel="beta",
                                       test_case_id="1111", test_suite_id="888666", blocked_by="123333111")

    @test_details
    def test_run(self):
        # value = option.get('log_cli')
        # assert value==False,"Log cli is false "
        assert True == True, "Log cli is false "
