# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Web compatibility test for amazon.com'
        self.enabled = False

    def login_amazon(self):
        try:
            wait(Pattern('amazon_sign_in_button.png'), 3)
        except FindError:
            logger.debug('Exit login')
        else:
            click(Pattern('amazon_sign_in_button.png'))
            time.sleep(3)
            paste(get_config_property('Amazon', 'username'))
            type(Key.ENTER)
            time.sleep(3)
            paste(get_config_property('Amazon', 'password'))
            type(Key.ENTER)
            time.sleep(3)
            amazon_logo = exists(Pattern('amazon_logo.png'), 5)
            assert_true(self, amazon_logo, 'Amazon logo exists')

    def run(self):
        navigate('www.amazon.com')
        keyword = 'Lord of the rings'
        try:
            wait(Pattern('amazon_logo.png'), 10)
        except FindError:
            logger.debug('Page was not loaded')

        else:
            self.login_amazon()
            time.sleep(4)
            type(Key.ESC)
            search = Pattern('amazon_search_button.png').target_offset(-100, 0)
            click(search)
            logger.debug('Amazon search')
            paste(keyword)
            type(Key.ENTER)

            amazon_search_result = Pattern('amazon_search_results.png')
            category = False
            found = False
            while not category:
                if exists(Pattern('amazon_books_result.png'), 0.25):
                    category = True
                    click(Pattern('amazon_books_result.png'))
                else:
                    scroll_down()
            assert_true(self, category, 'Book category was found')
            while not found:
                if exists(amazon_search_result, 0.25):
                    logger.debug('Book result is found')
                    found = True
                    break
                elif exists(Pattern('amazon_next_page.png'), 0.25):
                    logger.error('Searching result not found in page')
                    break
                else:
                    logger.debug('Scrolling down in page')
                    scroll_down()

            assert_true(self, found, 'Book result was found')
            amazon_cart = Pattern('amazon_cart.png')
            amazon_add_to_cart = Pattern('amazon_add_to_cart.png')
            amazon_delete_cart = Pattern('amazon_delete_cart.png')
            click(amazon_search_result)
            amazon_add_cart = exists(amazon_add_to_cart, 5)
            assert_true(self, amazon_add_cart, 'Cart image exists')
            logger.debug('Add product to cart')
            click(amazon_add_to_cart)
            amazon_car_image = exists(amazon_cart, 10)
            assert_true(self, amazon_car_image, 'Cart exists')
            logger.debug('Product was added to cart successfully')
            click(amazon_cart)
            time.sleep(4)
            delete_cart = exists(amazon_delete_cart, 10)
            assert_true(self, delete_cart, 'Delete cart exists')
            click(amazon_delete_cart)
            logger.debug('Product was successfully deleted from cart')
