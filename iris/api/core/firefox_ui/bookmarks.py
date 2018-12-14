# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.api.core.pattern import Pattern


class Bookmarks(object):
    class StarDialog(object):
        NEW_BOOKMARK = Pattern('editBookmarkPanelTitle_new_bookmark.png')
        EDIT_THIS_BOOKMARK = Pattern('editBookmarkPanelTitle_edit_this_bookmark.png')
        NAME_FIELD = Pattern('editBMPanel_nameRow.png')
        PANEL_FOLDER_DEFAULT_OPTION = Pattern('editBMPanel_folderMenuList_default_Other_Bookmarks.png')
        PANEL_FOLDERS_EXPANDER = Pattern('editBMPanel_foldersExpander.png')
        PANEL_FOLDERS_EXPANDER_UP = Pattern('editBMPanel_foldersExpander_Up.png')
        PANEL_OPTION_BOOKMARK_TOOLBAR = Pattern('editBMPanel_chooseFolderMenuItem_Bookmarks_Toolbar.png')
        PANEL_OPTION_BOOKMARK_MENU = Pattern('editBMPanel_chooseFolderMenuItem_Bookmarks_Menu.png')
        PANEL_OPTION_CHOOSE = Pattern('editBMPanel_chooseFolderMenuItem_Choose.png')
        NEW_FOLDER = Pattern('editBMPanel_newFolderButton.png')
        NEW_FOLDER_CREATED = Pattern('editBMPanel_newFolderCreated.png')
        TAGS_FIELD = Pattern('editBMPanel_tagsField.png')
        PANEL_TAGS_EXPANDER = Pattern('editBMPanel_tagsSelectorExpander.png')
        PANEL_TAGS_EXPANDER_UP = Pattern('editBMPanel_tagsSelectorExpander_Up.png')
        EDITOR_OPTION_CHECKED = Pattern('editBookmarkPanel_showForNewBookmarks_checked.png')
        EDITOR_OPTION_UNCHECKED = Pattern('editBookmarkPanel_showForNewBookmarks_unchecked.png')
        DONE = Pattern('editBookmarkPanelDoneButton.png')
        CANCEL = Pattern('editBookmarkPanelCancelButton.png')
        REMOVE_BOOKMARK = Pattern('editBookmarkPanelRemoveButton.png')
