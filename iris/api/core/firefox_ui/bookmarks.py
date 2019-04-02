# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.api.core.pattern import Pattern


class Bookmarks(object):
    class StarDialog(object):
        NEW_BOOKMARK = Pattern('edit_bookmark_panel_title_new_bookmark.png')
        EDIT_THIS_BOOKMARK = Pattern('edit_bookmark_panel_title_edit_this_bookmark.png')
        NAME_FIELD = Pattern('edit_bmpanel_namerow.png')
        PANEL_FOLDER_DEFAULT_OPTION = Pattern('edit_bmpanel_folder_menu_other_bookmarks.png')
        PANEL_FOLDERS_EXPANDER = Pattern('edit_bmpanel_folder_sex_pander.png')
        PANEL_FOLDERS_EXPANDER_UP = Pattern('edit_bmpanel_folder_sex_pander_up.png')
        PANEL_OPTION_BOOKMARK_TOOLBAR = Pattern('edit_bmpanel_choose_item_folder_menu_bookmarks_toolbar.png')
        PANEL_OPTION_BOOKMARK_MENU = Pattern('edit_bmpanel_choose_item_folder_bookmarks_menu.png')
        PANEL_OPTION_CHOOSE = Pattern('edit_bmpanel_folder_menu_item_choose.png')
        NEW_FOLDER = Pattern('edit_bmpanel_new_folder_button.png')
        NEW_FOLDER_CREATED = Pattern('edit_bmpanel_new_folder_created.png')
        TAGS_FIELD = Pattern('edit_bmpanel_tags_field.png')
        PANEL_TAGS_EXPANDER = Pattern('edit_bmpanel_tags_selector_expander.png')
        PANEL_TAGS_EXPANDER_UP = Pattern('edit_bmpanel_tags_selector_expander_up.png')
        EDITOR_OPTION_CHECKED = Pattern('edit_bmpanel_show_when_saving_checked.png')
        EDITOR_OPTION_UNCHECKED = Pattern('edit_bmpanel_show_when_saving_unchecked.png')
        DONE = Pattern('edit_bmpanel_done_button.png')
        CANCEL = Pattern('edit_bmpanel_cancel_button.png')
        REMOVE_BOOKMARK = Pattern('edit_bmpanel_remove_button.png')
