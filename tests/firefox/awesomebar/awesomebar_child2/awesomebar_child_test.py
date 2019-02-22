# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.



from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    name = "Awesomebar_child_test1"
    description="test_child."
    fx_version = "63"
    locale = "en-US, zh-CN, es-ES, de, fr, ru, ar, ko, pt-PT, vi, pl, tr, ro, ja"
    chanel="beta, release, nightly, esr, dev"
    test_case_id="1223232"
    test_suite_id="232323"
    blocked_by=""




    def test_run(self):
        # value = option.get('log_cli')
        # assert value==False,"Log cli is false "
        assert True==True,"Log cli is false "
