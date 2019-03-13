# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.api.core.pattern import Pattern


class Bookmarks(object):
    class StarDialog(object):
        NEW_BOOKMARK = Pattern('editbookmarkpaneltitle_new_bookmark.png')
        EDIT_THIS_BOOKMARK = Pattern('editbookmarkpaneltitle_edit_this_bookmark.png')
        NAME_FIELD = Pattern('editbmpanel_namerow.png')
        PANEL_FOLDER_DEFAULT_OPTION = Pattern('editbmpanel_foldermenulist_default_other_bookmarks.png')
        PANEL_FOLDERS_EXPANDER = Pattern('editbmpanel_foldersexpander.png')
        PANEL_FOLDERS_EXPANDER_UP = Pattern('editbmpanel_foldersexpander_up.png')
        PANEL_OPTION_BOOKMARK_TOOLBAR = Pattern('editbmpanel_choosefoldermenuitem_bookmarks_toolbar.png')
        PANEL_OPTION_BOOKMARK_MENU = Pattern('editbmpanel_choosefoldermenuitem_bookmarks_menu.png')
        PANEL_OPTION_CHOOSE = Pattern('editbmpanel_choosefoldermenuitem_choose.png')
        NEW_FOLDER = Pattern('editbmpanel_newfolderbutton.png')
        NEW_FOLDER_CREATED = Pattern('editbmpanel_newfoldercreated.png')
        TAGS_FIELD = Pattern('editbmpanel_tagsfield.png')
        PANEL_TAGS_EXPANDER = Pattern('editbmpanel_tagsselectorexpander.png')
        PANEL_TAGS_EXPANDER_UP = Pattern('editbmpanel_tagsselectorexpander_up.png')
        EDITOR_OPTION_CHECKED = Pattern('editbookmarkpanel_showfornewbookmarks_checked.png')
        EDITOR_OPTION_UNCHECKED = Pattern('editbookmarkpanel_showfornewbookmarks_unchecked.png')
        DONE = Pattern('editbookmarkpaneldonebutton.png')
        CANCEL = Pattern('editbookmarkpanelcancelbutton.png')
        REMOVE_BOOKMARK = Pattern('editbookmarkpanelremovebutton.png')
