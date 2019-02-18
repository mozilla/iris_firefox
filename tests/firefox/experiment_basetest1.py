

from targets.firefox.fx_testcase import *


class Test(FirefoxTest):




    def setup(self):
        self.meta='Check log level in pytest.ini file'
        self.title='lala'
        self.fx_version = '63'
        self.test_case_id = '123212223'
        self.test_suite_id = '1231'
        self.blocked_by="12311"



    def test_fixture_object(self,option):
        value = option.get('log_cli')
        assert   value,"Log cli is false "


