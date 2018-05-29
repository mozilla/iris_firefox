# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This test creates dynamic regions from patterns.'
        self.module_path = os.path.split(__file__)[0]
        self.assets = BaseTest.get_asset_path(self, self.module_path)
        self.module_name = os.path.split(__file__)[1].split('.py')[0]

    def run(self):
        """
        This is where your test logic goes.
        """

        r = create_region_from_patterns(left='home.png', right='library.png')
        print r.text()
        print r.x
        print r.y
        print r.w
        print r.h

        navigate(self.assets + '/' + self.module_name + '/test.htm')

        cat1 = 'cat1.png'
        cat2 = 'cat2.png'
        dog1 = 'dog1.png'
        dog2 = 'dog2.png'



        r1 = create_region_from_patterns(left=cat1, right=cat2)
        print r1.text()
        print r1.x
        print r1.y
        print r1.w
        print r1.h



        r2 = create_region_from_patterns(left=dog1, right=dog2)
        print r2.text()
        print r2.x
        print r2.y
        print r2.w
        print r2.h

        r3 = create_region_from_patterns(left='home.png', right='library.png')
        print r3.text()
        print r3.x
        print r3.y
        print r3.w
        print r3.h


        assert_true(self, True, 'test')
        return
