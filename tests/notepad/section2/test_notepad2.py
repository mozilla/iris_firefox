import pytest

from src.base.testcase import BaseTest


class Test(BaseTest):

    @pytest.mark.details(meta="Notepad Test experiment2",
                         description="This test is just an experiment for Notepad",
                         blocked_by="")
    def run(self):
        assert 1 == 1
