# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This test case checks the \'Drag and Drop within the awesomebar\' option, if it searches for'
                    ' the dropped string.',
        locale=['en-US'],
        test_case_id='117524',
        test_suite_id='1902'
    )
    def run(self, firefox):
        text_to_be_highlighted = Pattern('focus_text.png')
        highlighted_text = Pattern('focus_highlighted_text.png')
        drag_area = Pattern('focus_awesomebar.png')
        google_text_search = Pattern('focus_google_search.png')

        url = LocalWeb.FOCUS_TEST_SITE

        navigate(url)
        assert exists(LocalWeb.FOCUS_LOGO, 10), 'Page successfully loaded, focus logo found.'

        try:
            wait(text_to_be_highlighted, 10)
            logger.debug('The text is present on the page.')
            width, height = text_to_be_highlighted.get_size()
            location = image_find(text_to_be_highlighted)
            location_from = Location(location.x, location.y + height / 2)
            location_to = Location(location.x + width, location.y + height / 2)
            Mouse().drag_and_drop(location_from, location_to, duration=0.2)
        except FindError:
            raise FindError('The text is not present on the page, aborting.')

        try:
            wait(highlighted_text.similar(0.7), 10)
            logger.debug('Selected text is present on the page.')
        except FindError:
            raise FindError('Selected text is not present on the page, aborting.')

        try:
            drag_drop(highlighted_text, drag_area, duration=0.5)
        except FindError:
            raise FindError('Selected text could not be dragged and dropped, aborting.')

        assert exists(google_text_search.similar(0.6), 10), 'Google search successfully done.'
