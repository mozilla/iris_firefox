from iris2.core.screen.region import Region
from iris2.core.finder.pattern import Pattern

from iris2.testcase import *


class Test(BaseTest):

   def setUp(self):
        self.meta = 'Test_case example2'
        self.test_case_id = '119484'
        self.test_suite_id = '1902'

   def test_run(self):
       # print (self.meta)
       # mylogger.error('Testing error logs')
       assert 1==1
