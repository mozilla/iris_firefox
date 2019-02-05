
from targets.firefox.fx_testcase import *



class Test(FirefoxTest):

    def setup(self):
        self.meta = 'Image search test'
        self.test_case_id = '119484'
        self.test_suite_id = '1902'



    @pytest.mark.skipif(sys.platform == "darwin",
                        reason="Skip experimend:)")

    def test_run(self):
        region = Region(0, 40, 200, 100)
        region.highlight()
        # print(region.double_click(Pattern('test.png', application='firefox')))
        # print(region.exists('Project', 'Word found'))
        result=region.exists('Search a very')

        assert_true(self,result ,"Assert_message for Image search test ")

