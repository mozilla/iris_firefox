# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This test case checks the \'Drag and Drop within the awesomebar\' option, if it searches for' \
                    ' the dropped string.'
        self.test_case_id = '117524'
        self.test_suite_id = '1902'
        self.locales = ['en-US', 'es-ES', 'fr', 'de', 'ar', 'ru', 'pt-PT', 'vi', 'pl', 'tr', 'ro']

    def run(self):
        text_to_be_highlighted = Pattern('focus_text.png')
        highlighted_text = Pattern('focus_highlighted_text.png')
        drag_area = Pattern('focus_awesomebar.png')
        google_text_search = Pattern('focus_google_search.png')

        url = LocalWeb.FOCUS_TEST_SITE

        navigate(url)
        assert_true(self, exists(LocalWeb.FOCUS_LOGO, 10), 'Page successfully loaded, focus logo found.')

        # Highlight the selected area.
        try:
            wait(text_to_be_highlighted, 10)
            logger.debug('The text is present on the page.')
            width, height = get_image_size(text_to_be_highlighted)
            location = image_search(text_to_be_highlighted)
            location_from = Location(location.x, location.y + height / 2)
            location_to = Location(location.x + width, location.y + height / 2)
            drag_drop(location_from, location_to, 0.2)
        except FindError:
            raise FindError('The text is not present on the page, aborting.')

        # Wait for text to be highlighted.
        try:
            wait(highlighted_text.similar(0.7), 10)
            logger.debug('Selected text is present on the page.')
        except FindError:
            raise FindError('Selected text is not present on the page, aborting.')

        # Drag and drop highlighted text into awesomebar.
        try:
            drag_drop(highlighted_text, drag_area, 0.5)
        except FindError:
            raise FindError('Selected text could not be dragged and dropped, aborting.')

        assert_true(self, exists(google_text_search.similar(0.6), 10), 'Google search successfully done.')
