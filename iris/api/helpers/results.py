# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from logger.iris_logger import *

logger = getLogger(__name__)


def print_report_footer(passed, failed, skipped, total_time):
    total = passed + failed + skipped
    prefix = 'Passed: %s, Failed: %s, Skipped: %s, Total: %s' % (passed, failed, skipped, total)
    suffix = 'Total time: %s second(s)' % total_time
    separator = '\n' + '-' * 120 + '\n'
    logger.info('%s%s%s%s%s' % (separator, prefix, ' ' * (120 - (len(prefix) + len(suffix))), suffix, separator))


def format_outcome(outcome):
    if outcome:
        return 'PASSED'
    else:
        return 'FAILED'


def get_duration(start_time, end_time):
    return round(end_time - start_time, 2)
