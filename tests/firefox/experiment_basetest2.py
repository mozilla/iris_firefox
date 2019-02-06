from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    def setup(self):
        self.meta = 'Experiment 2'
        self.test_case_id = '3123123'
        self.test_suite_id = '1921312302'

    def test_run(self):

        assert_true(self,1 == 1,"Assert_message 1for experiment 2")
        assert_true(self,1 == 1,"Assert_message 2for experiment 2")

