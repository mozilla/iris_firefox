import pytest

from src.base.testcase import BaseTest


class Test(BaseTest):

    @pytest.mark.details(meta="Sample Test experiment2",
                         description="This test is just an experiment for Sample.",
                         custom_value="apple")
    def run(self):
        assert 1 == 1
