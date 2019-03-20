import sys

import pytest

from src.base.testcase import BaseTest
from src.core.api.finder.pattern import Pattern
from src.core.api.screen.region import find
from src.core.api.screen.screen import Rectangle


class Test(BaseTest):

    @pytest.mark.DETAILS(meta="Notepad Test experiment",
                                       description="This test is just an experiment for Notepad",
                                       blocked_by="232111")
    def test_run(self):
        find(Pattern('test.png'), Rectangle(0, 0, 100, 100))
        assert True == True, 'Assert message failed'
