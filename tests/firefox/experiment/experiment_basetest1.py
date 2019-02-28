# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    details = pytest.mark.DETAILS(meta="Test experiment_base_test1",
                                       description="This test is just an experiment.",
                                       fx_version="63", locale="en-US, zh-CN, es-ES, de", channel="beta",
                                       test_case_id="435344", test_suite_id="345444", blocked_by="")

    @details
    def test_run(self):
        # value = option.get('log_cli')
        # assert value==False,"Log cli is false "
        assert True == True, "Log cli is false "
