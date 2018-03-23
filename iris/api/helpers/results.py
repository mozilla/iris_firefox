# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


def format_outcome(outcome):
    if outcome:
        return 'PASS'
    else:
        return 'FAIL'


def get_duration(start_time, end_time):
    return round(end_time - start_time, 2)
