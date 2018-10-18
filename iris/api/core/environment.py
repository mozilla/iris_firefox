# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import pyperclip


class Env(object):

    @staticmethod
    def get_clipboard():
        """Return the content copied to clipboard."""
        return pyperclip.paste()
