# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris2.src.core.api.finder.pattern import Pattern


class FindToolbar(object):
    FIND_CLOSEBUTTON = Pattern('find_closebutton.png')
    FINDBAR_TEXTBOX = Pattern('findbar_textbox.png')
    FIND_PREVIOUS = Pattern('find_previous.png')
    FIND_NEXT = Pattern('find_next.png')
    HIGHLIGHT = Pattern('highlight.png')
    FIND_CASE_SENSITIVE = Pattern('find_case_sensitive.png')
    FIND_ENTIRE_WORD = Pattern('find_entire_word.png')
