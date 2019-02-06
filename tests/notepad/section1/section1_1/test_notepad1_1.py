from src.base.testcase import BaseTest
from src.core.api.finder.pattern import Pattern
from src.core.api.screen.region import find
from src.core.api.screen.screen import Rectangle


class Test(BaseTest):

    def test_run(self):
        find(Pattern('test.png'), Rectangle(0, 0, 100, 100))
        assert 1 == 1
