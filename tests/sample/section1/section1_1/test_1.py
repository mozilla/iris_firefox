import sys

import pytest

from src.base.testcase import BaseTest
from src.core.api.finder.pattern import Pattern
from src.core.api.screen.region import find
from src.core.api.screen.screen import Rectangle


class Test(BaseTest):

    @pytest.mark.details(meta="Sample Test experiment", locale=['en-US', 'es-ES', 'ro'],
                                       description="This test is just an experiment for Sample.",
                                       custom_value="banana")
    def run(self):
        find(Pattern('test.png'), Rectangle(0, 0, 100, 100))
        assert True == True, 'Assert message failed'
