import sys

import pytest

from src.base.testcase import BaseTest
from src.core.api.finder.pattern import Pattern
from src.core.api.screen.region import find
from src.core.api.screen.screen import Rectangle


class Test(BaseTest):

    @pytest.mark.skipif(sys.platform == "darwin",
                        reason="Skip experimend:)")
    def test_run(self):
        find(Pattern('test.png'), Rectangle(0, 0, 100, 100))
        assert True == True,'Assert message failed'
