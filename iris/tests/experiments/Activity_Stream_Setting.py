# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *
from api.helpers.awesome_bar import *
from sikuli import *




class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "Change Activity Stream Flag to true"


    def run(self):
        preference="browser.newtabpage.activity-stream.enabled"
        url="about:config"

        pattern=Pattern("home.png").similar(float(0.65))
        Screen =get_screen()

#search "home.png" image in the Screen
        if(Screen.find(pattern)):
            print"Home image found!!!"
        else:
            print"Home Image not found!!! "



#click on the search bar and access "about:config"
        type((pattern.targetOffset(400,0)), url+Key.ENTER)

        #enable/disable preferances //assuming that activity stream is disabled
        type((Pattern("searchIcon")), preference+Key.ENTER)
        type(Key.TAB)
        type(Key.ENTER)

        #switch to new tab and check if activity stream is enabled
        new_tab()

        if(Screen.find(Pattern("Top_Sites.png"))):
            print"Activity stream is enabled!!!"
        else:
            print"Something went wrong..."









