from src.base.testcase import BaseTest


class Test(BaseTest):
    name = "Test experiment"
    description = "This test is just an experiment."
    fx_version = "63"
    locale = "en-US, zh-CN, es-ES, de"
    chanel = "beta"
    test_case_id = "435344"
    test_suite_id = "345444"
    blocked_by = ""

    def test_notepad2_1(self):
        assert 1 == 1


    def test_notepad2_2(self):
        assert True == False ,'Assertion should be True'


