# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Paste .jpeg File in demopage',
        locale=['en-US'],
        test_case_id='165096',
        test_suite_id='102',
        blocked_by={'id': '1288773', 'platform': OSPlatform.ALL}
    )
    def run(self, firefox):
        paste_jpeg_button_pattern = Pattern('paste_jpeg_file_button.png')
        paste_jpeg_file_selected_button_pattern = Pattern('paste_jpeg_file_selected_button.png')
        drop_here_pattern = Pattern('drop_here.png')
        not_matching_message_pattern = Pattern('not_matching_message.png')
        matching_message_pattern = Pattern('matching_message_precise.png')
        jpg_file_pattern = Pattern('jpg_file.png')
        pdf_file_pattern = Pattern('pdf_file.png')
        scroll = Mouse().scroll

        drag_and_drop_duration = 3
        folderpath = self.get_asset_path('')

        navigate('https://mystor.github.io/dragndrop/')

        paste_jpeg_file_button_displayed = exists(paste_jpeg_button_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert paste_jpeg_file_button_displayed, 'The demo website loaded successfully'

        click(paste_jpeg_button_pattern)

        paste_jpeg_option_selected = exists(paste_jpeg_file_selected_button_pattern)
        assert paste_jpeg_option_selected, 'The paste-jpeg-file changed color to red which indicates that ' \
                                           'it has been selected.'

        matching_block_available = scroll_until_pattern_found(not_matching_message_pattern, scroll, (-25,), 20, 1)
        assert matching_block_available, 'The drop result verification area is displayed on the page'

        not_matching_message_location = find(not_matching_message_pattern)
        not_matching_message_width, not_matching_message_height = not_matching_message_pattern.get_size()
        not_matching_region = Region(not_matching_message_location.x, not_matching_message_location.y,
                                     width=not_matching_message_width, height=not_matching_message_height)

        matching_message_width, matching_message_height = matching_message_pattern.get_size()
        matching_region = Region(not_matching_message_location.x, not_matching_message_location.y,
                                 width=matching_message_width + 10, height=matching_message_height * 2)

        select_file_in_folder(folderpath, jpg_file_pattern, edit_copy)

        drop_here_available = exists(drop_here_pattern)
        assert drop_here_available, '"Drop here" pattern available'

        click(drop_here_pattern, drag_and_drop_duration)

        edit_paste()

        matching_message_displayed = exists(matching_message_pattern, region=matching_region)
        assert matching_message_displayed, 'Matching appears under the "Drop Stuff Here" area and expected' \
                                           'result is identical to result. '

        select_file_in_folder(folderpath, pdf_file_pattern, edit_copy)

        drop_here_available = exists(drop_here_pattern)
        assert drop_here_available, '"Drop here" pattern available'

        click(drop_here_pattern, drag_and_drop_duration)

        edit_paste()

        not_matching_message_displayed = exists(not_matching_message_pattern, region=not_matching_region)
        assert not_matching_message_displayed, 'Not Matching appears under the "Drop Stuff Here" area and ' \
                                               'expected result is different from result.'

        type(Key.ESC)
