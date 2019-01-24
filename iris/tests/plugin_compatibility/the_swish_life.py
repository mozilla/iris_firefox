from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = '"The Swish Life" is properly loaded and works as intended'
        self.test_case_id = '125532'
        self.test_suite_id = '2074'
        self.locales = ['en-US']

    def run(self):
        the_swish_life_tab_pattern = Pattern('the_swish_life_tab.png')
        fashion_tag_pattern = Pattern('fashion_tag.png')
        fashion_page_pattern = Pattern('fashion_page.png')
        the_home_button_pattern = Pattern('the_home_button.png')

        navigate('http://theswishlife.com/')

        window_opened = exists(the_swish_life_tab_pattern, DEFAULT_FIREFOX_TIMEOUT * 3)
        assert_true(self, window_opened, 'The Swish Life home page opened')

        page_end()

        fashion_tag_exists = exists(fashion_tag_pattern)
        if not fashion_tag_exists:
            assert_false(self, fashion_tag_exists, 'The "Fashion" tag exists')

        click(fashion_tag_pattern)

        fashion_page_opened = exists(fashion_page_pattern, DEFAULT_FIREFOX_TIMEOUT * 3)
        assert_true(self, fashion_page_opened, 'The "Fashion" page is opened')

        click(the_home_button_pattern)

        home_page_label = exists(fashion_page_pattern, DEFAULT_FIREFOX_TIMEOUT * 3)
        assert_true(self, home_page_label, 'Return to the Swish Life home page. The website and the browser are stable')

