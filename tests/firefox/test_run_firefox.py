
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    # @pytest.mark.skipif(sys.platform == "darwin", reason="Skip experiment :)")
    def test_run(self):
        time.sleep(10)
        assert 1 == 1

