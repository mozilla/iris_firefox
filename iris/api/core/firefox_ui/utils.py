# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.api.core.pattern import Pattern


class Utils(object):
    # Checkbox.
    CHECKEDBOX = Pattern('checked_box.png')
    UNCHECKEDBOX = Pattern('unchecked_box.png')

    # Back Arrow.
    LIBRARY_BACK_BUTTON = Pattern('subview_button_back.png')

    TOP_SITES = Pattern('top_sites.png')

    SAVE_BUTTON_GOOGLE = Pattern('save_button_google.png')

    # Folder view.
    NEW_FOLDER = Pattern('new_folder.png')
    NEW_FOLDER_HIGHLIGHTED = Pattern('new_folder_highlighted.png')
    SELECT_FOLDER = Pattern('select_folder.png')
    NEW_DOWNLOADS_FOLDER_HIGHLIGHTED = Pattern('new_downloads_folder_highlighted.png')


