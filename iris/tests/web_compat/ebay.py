# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from test_case import *



class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "Web compability test for ebay"


    def login_ebay(self):
        try:
            wait("ebay_sign_in.png",10)
        except:
            logger.debug( "Exit login")
        else:
            click('ebay_sign_in.png')
            wait('ebay_table_login.png',10)
            click('ebay_table_login.png')
            time.sleep(2)
            type(Key.TAB)
            type(Key.TAB)
            paste(get_credential("Ebay","username"))
            time.sleep(5)
            type(Key.TAB)
            paste(get_credential("Ebay","password"))
            type(Key.ENTER)
            time.sleep(5)
            type(Key.ESC)
            if exists('ebay_search.png',10):
                logger.debug( "Login was succesfully performed")
            else:
                logger.debug( "Something went wrong and the user was not logged in")




    def run(self):
        url="www.ebay.com"
        keyword="shoes"


        navigate(url)

        try:
            wait('ebay_search.png',10)
            logger.debug( "Page load successfuly")
        except:
            logger.error ("Can't find Ebay image in page, aborting test.")

        else:
            self.login_ebay()
            type(keyword)
            logger.debug( "Search product:")
            type(Key.ENTER)
            time.sleep(5)

            for x in range(5):
               logger.debug("Scrolling down!!")
               scroll_down()
               time.sleep(0.25)

            if exists('ebay_search.png',5):
               logger.debug("Scroll down was not performed")
            else:
               for x in range(5):
                   logger.debug("Scrolling up!!")
                   scroll_up()
                   time.sleep(0.25)
            if exists('ebay_search.png',5):
               logger.debug('Page was scrolled back up!!')
               page_text = get_firefox_region().text()
               related_results=['Categories','Brand']
               found = False
               for word in related_results:
                   if word in page_text:
                       found = True
                       break
               if found:
                   logger.debug('Results are displayed!!')
                   search=Sikuli.Pattern("ebay_filter_results.png").targetOffset(0,100)
                   if exists('ebay_filter_results.png',5):
                       logger.debug('Select product!!')
                       click(search)
                       time.sleep(3)
                       print "PASS"

                   else:
                       logger.error('Product not selected!!')
                       print "FAIL"



               else:
                   logger.error('No results were displayed!!')
                   print "FAIL"

            else:
               logger.error('Page was not scrolled back up!!')
               print "FAIL"








