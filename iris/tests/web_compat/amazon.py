# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = "Web compability test for amazon.com"
        self.enable = False

    def login_amazon(self):
        try:
            wait("amazon_sign_in_button.png", 3)
        except:
            logger.debug("Exit login")
        else:
            click("amazon_sign_in_button.png")
            time.sleep(3)
            paste(get_credential("Amazon", "username"))
            type(Key.ENTER)
            time.sleep(3)
            paste(get_credential("Amazon", "password"))
            type(Key.ENTER)
            time.sleep(3)
            if exists("amazon_logo.png", 5):
                logger.debug("Login was succesfully performed")
            else:
                logger.debug("Something went wrong and the user was not logged in")

    def run(self):
        url = "www.amazon.com"
        navigate(url)
        keyword = "Lord of the rings"
        try:
            wait("amazon_logo.png", 10)
        except:
            logger.debug("Page was not loaded")

        else:
            self.login_amazon()
            time.sleep(4)
            type(Key.ESC)
            search = Pattern("amazon_search_button.png").targetOffset(-100, 0)
            click(search)
            logger.debug("Amazon search")
            paste(keyword)
            type(Key.ENTER)

            amazon_search_result = Pattern('amazon_search_results.png')

            found = False
            while found == False:
                if exists(amazon_search_result, 0.25):
                    logger.debug("Book result is found")
                    found = True
                    break
                elif exists('amazon_next_page.png', 0.25):
                    logger.error("Searching result not found in page")
                    break

                else:
                    logger.debug("Scrolling down in page")
                    scroll_down()

            if found:
                amazon_cart = Pattern('amazon_cart.png')
                amazon_add_to_cart = Pattern('amazon_add_to_cart.png')
                amazon_delete_cart = Pattern('amazon_delete_cart.png')
                click(amazon_search_result)
                if exists(amazon_add_to_cart, 5):
                    logger.debug("Add product to cart")
                    click(amazon_add_to_cart)
                    if exists(amazon_cart, 10):
                        logger.debug("Product was added to cart successfully")
                        click(amazon_cart)
                        time.sleep(4)
                        if exists(amazon_delete_cart, 10):
                            click(amazon_delete_cart)
                            logger.debug("Product was successfully deleted from cart")
                            time.sleep(4)
                            print "PASS"

                else:
                    logger.debug('Product was not added to cart')
                    print "FAIL"
            else:
                logger.debug("Image not found")
                print "FAIL"
