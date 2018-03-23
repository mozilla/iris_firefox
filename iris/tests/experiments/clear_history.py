from test_case import *


class test(base_test):
    def __init__(self, app):
        base_test.__init__(self, app)
        self.meta = "This is a test for clearing browser history"

    def run(self):

        url = "https://www.amazon.com"
        amazon_history = "amazon_history.png"

        navigate(url)

        try:
            wait("amazon.png", 10)
        except:
            logger.error("Can't find Amazon image in page, aborting test.")
            return

        # The various calls to time.sleep are necessary to
        # account for lag times incurred by underlying operations.
        # We can always switch to image detection as a mechanism to
        # confirm presence of UI before interaction, but that
        # has its own cost.

        clear_recent_history()
        time.sleep(2)
        press("enter")
        time.sleep(2)

        # The click here is required, because the Firefox window loses
        # focus after invoking the above dialog, and without it,
        # the keyboard shortcuts don't work

        click("home.png")

        # Navigate to new page; otherwise, our bitmap for the history item
        # looks identical to the image in the title bar and we'll get
        # a false match
        navigate("about:blank")

        history_sidebar()
        time.sleep(2)
        typewrite("amazon")

        if exists(amazon_history, 5):
            print ("FAIL")
        else:
            print ("PASS")
