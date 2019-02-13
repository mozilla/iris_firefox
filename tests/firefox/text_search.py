
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    def test_run(self):
        time.sleep(10)
        assert 1 == 1

