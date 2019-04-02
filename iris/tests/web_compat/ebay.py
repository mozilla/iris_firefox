# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.assets = os.path.join(os.path.split(__file__)[0], 'assets')
        self.meta = 'Web compatibility test for eBay'
        self.enabled = False

    def login_ebay(self):
        login_success = False
        try:
            wait(Pattern('ebay_sign_in.png'), 10)
        except FindError:
            logger.debug('Exit login')
            return login_success
        else:
            click(Pattern('ebay_sign_in.png'))
            try:
                wait(Pattern('ebay_table_login.png'), 10)
            except FindError:
                logger.debug('Something went wrong with login')
                return login_success
            click(Pattern('ebay_table_login.png'))
            time.sleep(2)
            type(Key.TAB)
            type(Key.TAB)
            paste(get_config_property('Ebay', 'username'))
            time.sleep(5)
            type(Key.TAB)
            paste(get_config_property('Ebay', 'password'))
            type(Key.ENTER)
            time.sleep(5)
            type(Key.ESC)
            ebay_search = exists(Pattern('ebay_search.png'), 10)
            assert_true(self, ebay_search, 'User successfully logged in')
            login_success = True

        return login_success

    def run(self):
        url = 'www.ebay.com'
        keyword = 'shoes'

        navigate(url)

        try:
            wait(Pattern('ebay_search.png'), 15)
            logger.debug('Page load successfully')
        except FindError:
            raise FindError('Can\'t find eBay image in page, aborting test.')
        else:
            if not self.login_ebay():
                return
            type(keyword)
            logger.debug('Search product:')
            type(Key.ENTER)
            time.sleep(5)

            for x in range(5):
                logger.debug('Scrolling down')
                scroll_down()
                time.sleep(0.25)

            ebay_search = exists(Pattern('ebay_search.png'), 5)
            assert_false(self, ebay_search, 'eBay search bar exists')
            for x in range(5):
                logger.debug('Scrolling up')
                scroll_up()
                time.sleep(0.25)
            ebay_search = exists(Pattern('ebay_search.png'), 5)
            assert_true(self, ebay_search, 'eBay search bar exists')
            logger.debug('Page was scrolled back up')
            screen = get_firefox_region()
            product_region = Region(screen.x(), screen.y(), screen.width() / 4, screen.height())
            related_results = ['Categories', 'Brand']
            found = False
            for word in related_results:
                if word in product_region.text():
                    logger.debug('Word is %s' % word)
                    found = True
                    break
            assert_true(self, found, 'Text found in page')
            logger.debug('Results are displayed')
            search = Pattern('ebay_filter_results.png').target_offset(0, 100)
            ebay_filter = exists(Pattern('ebay_filter_results.png'), 5)
            assert_true(self, ebay_filter, 'Filter button found in page')
            logger.debug('Select product')
            click(search)
            back_to_search_results = exists(Pattern('ebay_back_to_search.png'), 5)
            assert_true(self, back_to_search_results, 'Product successfully selected')
