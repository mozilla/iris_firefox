# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.api.core.pattern import Pattern


class FindToolbar(object):
    FIND_CLOSEBUTTON = Pattern('find_closebutton.png')
    FINDBAR_TEXTBOX = Pattern('findbar_textbox.png')
    FIND_PREVIOUS = Pattern('find_previous.png')
    FIND_NEXT = Pattern('find_next.png')
    HIGHLIGHT = Pattern('highlight.png')
    FIND_CASE_SENSITIVE = Pattern('find_case_sensitive.png')
    FIND_ENTIRE_WORD = Pattern('find_entire_word.png')
    QUICK_FIND_LABEL = Pattern('quick_find_label.png')
    QUICK_FIND_LINKS_ONLY_LABEL = Pattern('quick_find_links_only_label.png')
    FIND_STATUS_PHRASE_NOT_FOUND = Pattern('findbar_find_status_phrase_not_found.png')
