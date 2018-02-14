# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import datetime

today = datetime.date.today()


def begin_results_file():
    f = open('testresults.txt', 'w')
    f.write('Test run results for %s\n' % today)
    f.close()
    return


def append_results_file(result_msg):
    f = open('testresults.txt', 'a')
    f.write(result_msg + '\n')
    f.close()
    return


def conclude_results_file():
    f = open('testresults.txt', 'a')
    f.write('This concludes our testing for %s\n' % today)
    f.close()
    return
