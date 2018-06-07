# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This test creates dynamic regions from patterns.'
        # Disable until issue #586 is fixed
        self.exclude = Platform.ALL

    def run(self):

        cat1 = 'cat1.png'
        cat2 = 'cat2.png'
        dog1 = 'dog1.png'
        dog2 = 'dog2.png'

        r = create_region_from_patterns(left='home.png', right='library.png')
        logger.debug('Region x, y, w, h: %s %s %s %s' % (r.x, r.y, r.w, r.h))
        logger.debug('Text in URL bar: %s' % r.text(with_image_processing=True))

        return

        test_url = self.get_asset_path(__file__, 'test.htm')
        navigate(test_url)
        logger.debug('Navigate to URL: %s' % test_url)
        logger.debug('Text in URL bar: %s' % r.text(with_image_processing=True))

        test_string_cat = 'This is a cat'
        r1 = create_region_from_patterns(left=cat1, right=cat2)
        text = r1.text()
        logger.debug('Region x, y, w, h: %s %s %s %s' % (r1.x, r1.y, r1.w, r1.h))
        logger.debug('Text in region: %s' % text)
        assert_true(self, test_string_cat in text, 'Can find cat text')
        assert_false(self, 'Dog' in text, 'Should not find Dog in cat text')

        test_string_dog = 'This is a dog'
        r2 = create_region_from_patterns(left=dog1, right=dog2)
        text = r2.text()
        logger.debug('Region x, y, w, h: %s %s %s %s' % (r2.x, r2.y, r2.w, r2.h))
        logger.debug('Text in region: %s' % text)
        assert_true(self, test_string_dog in text, 'Can find dog text')
        assert_false(self, 'Cat' in text, 'Should not find Cat in dog text')

        navigate('google.com')
        logger.debug('Navigate to URL: google.com')
        logger.debug('Text in URL bar: %s' % r.text())

        navigate(test_url)
        logger.debug('Navigate to URL: %s' % test_url)
        logger.debug('Text in URL bar: %s' % r.text())

        navigate('12345')
        logger.debug('Navigate to URL: 12345')
        logger.debug('Text in URL bar: %s' % r.text())

        return
